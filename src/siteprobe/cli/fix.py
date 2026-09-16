import json
from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from siteprobe.core.engine import AuditResult
from siteprobe.models.remediation import RemediationPlan
from siteprobe.remediation.executor import RemediationExecutor
from siteprobe.remediation.planner import RemediationPlanner


def fix_command(
    audit_path: str = typer.Argument(..., help="Path to audit.json produced by siteprobe audit"),
    repo: str = typer.Option(".", "--repo", "-r", help="Target source repository or directory to apply fixes"),
) -> None:
    console = Console()
    p = Path(audit_path)
    if not p.is_file():
        console.print(f"[red]Error: Audit file not found: {audit_path}[/red]")
        raise typer.Exit(code=1)

    console.print(Panel(f"[bold green]SiteProbe Remediation Engine (Fix Mode)[/bold green]\nAudit Source: [cyan]{audit_path}[/cyan] | Target: [yellow]{repo}[/yellow]"))

    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
        audit_res = AuditResult.model_validate(data)

    plan = RemediationPlanner.create_plan(audit_res.site_url, audit_res.findings)
    console.print(f"Discovered [bold cyan]{len(plan.actions)}[/bold cyan] total remediation tasks:")
    console.print(f"  • Safe Autofix: [green]{plan.safe_count}[/green]")
    console.print(f"  • Review Recommended: [yellow]{plan.review_count}[/yellow]")
    console.print(f"  • Manual Only: [dim]{plan.manual_count}[/dim]\n")

    if plan.safe_count == 0:
        console.print("[yellow]No safe automatic fixes available for these findings.[/yellow]")
        return

    executor = RemediationExecutor(repo)
    report = executor.apply_safe_fixes(plan)

    console.print(f"[bold green]✓ Applied {report.applied_count} safe fixes![/bold green]\n")

    if report.diffs:
        console.print("[bold]Modified Files & Diffs:[/bold]")
        for file_name, diff_text in report.diffs.items():
            console.print(Panel(diff_text, title=f"File: {file_name}", border_style="green"))

    console.print("[bold cyan]Next step:[/bold cyan] Run [dim]siteprobe verify " + audit_path + " --repo " + repo + "[/dim] to verify the changes.")
