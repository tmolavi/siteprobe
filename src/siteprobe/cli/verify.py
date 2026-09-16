import json
from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from siteprobe.core.engine import AuditResult
from siteprobe.verification.verifier import FixVerifier


def verify_command(
    audit_path: str = typer.Argument(..., help="Path to audit.json file"),
    repo: str = typer.Option(".", "--repo", "-r", help="Target source repository or directory to verify against"),
) -> None:
    console = Console()
    p = Path(audit_path)
    if not p.is_file():
        console.print(f"[red]Error: Audit file not found: {audit_path}[/red]")
        raise typer.Exit(code=1)

    console.print(Panel(f"[bold green]SiteProbe Verification Engine[/bold green]\nAudit: [cyan]{audit_path}[/cyan] | Workspace: [yellow]{repo}[/yellow]"))

    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
        audit_res = AuditResult.model_validate(data)

    results = FixVerifier.verify_local_changes(audit_res.findings, repo)

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Rule ID")
    table.add_column("Status", justify="center")
    table.add_column("Verification Message")

    fixed_count = 0
    for r in results:
        status_color = "green" if r.status.value == "FIXED" else ("red" if r.status.value == "FAILED" else "dim")
        table.add_row(r.finding_id, f"[{status_color}]{r.status.value}[/{status_color}]", r.message)
        if r.status.value == "FIXED":
            fixed_count += 1

    console.print(table)
    console.print(f"\n[bold]Verification Complete:[/bold] [green]{fixed_count}[/green] fixed out of {len(results)} evaluated items.\n")
