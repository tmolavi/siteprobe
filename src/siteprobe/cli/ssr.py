import sys
import httpx
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from siteprobe.checks.technical.ssr import analyze_ssr


def ssr_command(
    url: str = typer.Argument(..., help="Target website URL to inspect for SSR/CSR rendering"),
    timeout: float = typer.Option(10.0, "--timeout", "-t", help="HTTP request timeout in seconds"),
) -> None:
    """Analyze raw server response to diagnose SSR, client-side hydration, and empty SPA shells."""
    console = Console()
    console.print(Panel(f"[bold cyan]SiteProbe SSR & Rendering Inspector[/bold cyan]\nTarget: [yellow]{url}[/yellow]"))

    with console.status("[bold blue]Fetching initial raw server HTML...[/bold blue]", spinner="dots"):
        try:
            headers = {"User-Agent": "SiteProbe/0.1.1 SSR-Inspector"}
            resp = httpx.get(url, headers=headers, follow_redirects=True, timeout=timeout)
            html = resp.text
            status_code = resp.status_code
        except Exception as e:
            console.print(f"[bold red]Failed to fetch target URL:[/bold red] {e}")
            raise typer.Exit(code=1)

    analysis = analyze_ssr(html)

    # Status color
    if analysis.rendering_mode in ("FULL_SSR", "HYDRATED_SSR", "STATIC_HTML", "ISLANDS_SSR"):
        mode_style = "bold green"
    else:
        mode_style = "bold red"

    console.print(f"\n[bold]HTTP Status:[/bold] {status_code}")
    console.print(f"[bold]Detected Rendering Mode:[/bold] [{mode_style}]{analysis.rendering_mode}[/{mode_style}]")
    console.print(f"[bold]Detected Framework:[/bold] [cyan]{analysis.framework}[/cyan]")
    console.print(f"[bold]Raw HTML Word Count:[/bold] {analysis.raw_word_count} words")
    console.print(f"[bold]Hydration Payload:[/bold] {'Yes (' + str(analysis.hydration_payload_size_bytes) + ' bytes)' if analysis.has_hydration_payload else 'No'}\n")

    # Raw SEO Tags Table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Critical SEO Tag (in Raw HTML)")
    table.add_column("Presence", justify="center")
    table.add_column("Impact on Crawlers")

    for tag, present in analysis.raw_seo_tags.items():
        status = "[green]PRESENT[/green]" if present else "[red]MISSING (JS Required)[/red]"
        impact = "Indexable by all search & AI bots" if present else "May fail indexing on bots with limited JS rendering budget"
        table.add_row(f"<{tag}>", status, impact)

    console.print(table)

    if analysis.details:
        console.print("\n[bold]Diagnostic Signals:[/bold]")
        for d in analysis.details:
            console.print(f"  • {d}")

    # Summary Advice
    if analysis.rendering_mode == "CLIENT_SIDE_SPA":
        console.print(Panel(
            "[bold red]Warning: Client-Side Only Rendering (SPA) Detected[/bold red]\n"
            "Search engines (Googlebot, Bingbot) and AI retrieval crawlers (OAI-SearchBot, PerplexityBot) "
            "may not see your main content during their initial crawl pass. Consider adopting Server-Side Rendering (Next.js/Nuxt) or pre-rendering/SSG.",
            border_style="red"
        ))
    else:
        console.print(Panel(
            "[bold green]Optimal for Search & AI Crawlers[/bold green]\n"
            "Content and structural signals are directly accessible in the initial server HTML response without requiring client-side JavaScript execution.",
            border_style="green"
        ))
