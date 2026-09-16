import asyncio
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from siteprobe.core.config import load_config
from siteprobe.core.engine import AuditEngine
from siteprobe.models.config import CrawlConfig, SiteConfig
from siteprobe.models.finding import Severity
from siteprobe.reporting.html_reporter import HtmlReporter
from siteprobe.reporting.json_reporter import JsonReporter
from siteprobe.reporting.markdown_reporter import MarkdownReporter


def audit_command(
    url: str = typer.Argument(..., help="Target website URL (e.g. https://example.com)"),
    max_pages: int = typer.Option(50, "--max-pages", "-m", help="Maximum pages to crawl"),
    lang: str = typer.Option("en", "--lang", "-l", help="Language code (en, fa, tr)"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Directory or file path for reports"),
    format: str = typer.Option("html", "--format", "-f", help="Output format: html, json, markdown"),
    lighthouse: bool = typer.Option(False, "--lighthouse", help="Run lab performance audit using Lighthouse if available"),
    accessibility: bool = typer.Option(False, "--accessibility", help="Run deep axe-core checks via Playwright if available"),
) -> None:
    console = Console()
    console.print(Panel(f"[bold green]SiteProbe Autonomous Auditor[/bold green]\nTarget: [cyan]{url}[/cyan] | Lang: [magenta]{lang}[/magenta] | Max Pages: [yellow]{max_pages}[/yellow]"))

    cfg = load_config()
    cfg.site.url = url
    cfg.site.language = lang
    cfg.crawl.max_pages = max_pages

    engine = AuditEngine(config=cfg, language=lang)

    with console.status("[bold blue]Crawling website and running audit checks...[/bold blue]", spinner="dots"):
        result = asyncio.run(engine.run_audit(url))

    # Display Executive Summary Table
    console.print("\n[bold]📊 Audit Results Summary[/bold]")
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Category")
    table.add_column("Score", justify="center")
    table.add_column("Issues (Crit / High / Med / Low)")

    for cat_name, cs in result.scores.category_scores.items():
        score_style = "green" if cs.score >= 80 else ("yellow" if cs.score >= 60 else "red")
        issues_str = f"{cs.critical_count} / {cs.high_count} / {cs.medium_count} / {cs.low_count}"
        table.add_row(cat_name.replace("_", " ").title(), f"[{score_style}]{cs.score}[/{score_style}]", issues_str)

    console.print(table)

    # Score Callout
    overall_style = "green" if result.scores.overall_score >= 80 else ("yellow" if result.scores.overall_score >= 60 else "red")
    console.print(f"\n[bold]Overall Quality Score:[/bold] [{overall_style} bold]{result.scores.overall_score} / 100[/{overall_style} bold]")
    console.print(f"[bold]GEO & AI Search Readiness:[/bold] [cyan bold]{result.scores.geo_score} / 100[/cyan bold] (Pillars: Bots {result.scores.geo_score_breakdown.get('ai_crawler_access', 0)}/40, llms.txt {result.scores.geo_score_breakdown.get('llms_txt_presence', 0)}/20)")
    console.print(f"[dim]Total Crawled: {result.crawl_summary.total_crawled} pages in {result.crawl_summary.crawl_duration_seconds}s | Findings: {len(result.findings)}[/dim]\n")

    # Output report
    out_dir = Path(output) if output else Path("./siteprobe-report")
    out_dir.mkdir(parents=True, exist_ok=True)

    json_file = out_dir / "audit.json"
    html_file = out_dir / "audit.html"
    md_file = out_dir / "audit.md"

    JsonReporter.save(result, json_file)
    HtmlReporter.save(result, html_file)
    MarkdownReporter.save(result, md_file)

    console.print(f"[green]✓[/green] JSON report saved to: [bold]{json_file}[/bold]")
    console.print(f"[green]✓[/green] HTML dashboard saved to: [bold]{html_file}[/bold]")
    console.print(f"[green]✓[/green] Markdown summary saved to: [bold]{md_file}[/bold]\n")
