import json
from pathlib import Path
from typing import List, Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from siteprobe.models.finding import Finding
from siteprobe.updates.constants import (
    DIAGNOSTIC_INSUFFICIENT_DATA,
    DIAGNOSTIC_MANUAL_ACTION,
    DIAGNOSTIC_NO_CHANGE,
    DIAGNOSTIC_PERFORMANCE_CHANGE,
    DIAGNOSTIC_TECHNICAL_ISSUE,
    EVENT_NAME,
    ROLLOUT_END,
    ROLLOUT_START,
)
from siteprobe.updates.triage import UpdateImpactTriage


def update_triage_command(
    csv: Optional[str] = typer.Option(
        None, "--csv", "-c", help="Path to Google Search Console CSV export file"
    ),
    audit_file: Optional[str] = typer.Option(
        None, "--audit-file", "-a", help="Path to existing SiteProbe audit.json to evaluate technical issues"
    ),
    manual_action: str = typer.Option(
        "unknown",
        "--manual-action",
        "-m",
        help="Search Console verified manual action status: 'true', 'false', or 'unknown'",
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="File path to save JSON triage report"
    ),
    json_output: bool = typer.Option(
        False, "--json", help="Output machine-readable JSON to stdout"
    ),
) -> None:
    """
    Triage Google Search Console performance shifts around algorithm updates.
    Distinguishes observed performance drops, technical website issues, manual actions,
    and possible update correlations.
    """
    console = Console()

    # Parse manual action flag
    norm_ma = manual_action.strip().lower()
    if norm_ma in ("true", "1", "yes"):
        ma_reported: Optional[bool] = True
    elif norm_ma in ("false", "0", "no"):
        ma_reported = False
    else:
        ma_reported = None

    # Load technical findings if audit file provided
    findings: List[Finding] = []
    if audit_file:
        audit_path = Path(audit_file)
        if audit_path.exists():
            try:
                data = json.loads(audit_path.read_text(encoding="utf-8"))
                raw_findings = data.get("findings", [])
                findings = [Finding.model_validate(f) for f in raw_findings]
            except Exception as e:
                console.print(f"[yellow]Warning: Could not load audit file '{audit_file}': {e}[/yellow]")
        else:
            console.print(f"[yellow]Warning: Audit file '{audit_file}' not found.[/yellow]")

    # Run Triage
    triage = UpdateImpactTriage(
        csv_source=csv,
        manual_action_reported=ma_reported,
        audit_findings=findings,
    )
    result = triage.run()

    # If raw JSON requested
    if json_output:
        typer.echo(result.model_dump_json(indent=2))
        return

    # Terminal UI
    console.print(Panel(
        f"[bold cyan]SiteProbe Google Update Impact Triage[/bold cyan]\n"
        f"Event: [bold white]{EVENT_NAME}[/bold white]\n"
        f"Official Rollout: [magenta]{ROLLOUT_START}[/magenta] through [magenta]{ROLLOUT_END}[/magenta]",
        title="Google Algorithm Update Analysis",
    ))

    # Diagnostic Badge
    diag_colors = {
        DIAGNOSTIC_NO_CHANGE: "bold green",
        DIAGNOSTIC_PERFORMANCE_CHANGE: "bold magenta",
        DIAGNOSTIC_TECHNICAL_ISSUE: "bold yellow",
        DIAGNOSTIC_MANUAL_ACTION: "bold red",
        DIAGNOSTIC_INSUFFICIENT_DATA: "bold yellow",
    }
    color = diag_colors.get(result.diagnostic, "bold cyan")
    console.print(f"\nDiagnostic Classification: [{color}]{result.diagnostic}[/{color}]")
    console.print(f"Reason: [dim]{result.diagnostic_reason}[/dim]\n")

    # Windows Comparison Table
    if result.pre_metrics and result.rollout_metrics:
        table = Table(title="Frozen Comparison Windows", header_style="bold cyan")
        table.add_column("Window", style="bold")
        table.add_column("Date Range", style="dim")
        table.add_column("Days", justify="center")
        table.add_column("Total Clicks", justify="right")
        table.add_column("Total Impressions", justify="right")
        table.add_column("CTR", justify="right")
        table.add_column("Avg Position", justify="right")

        for m in [result.pre_metrics, result.rollout_metrics, result.completion_day_metrics, result.post_metrics]:
            if not m:
                continue
            status_flag = " [green]✓[/green]" if m.is_complete else " [yellow](incomplete)[/yellow]"
            pos_str = f"{m.avg_position:.1f}" if m.avg_position else "N/A"
            table.add_row(
                m.window_name + status_flag,
                f"{m.start_date} to {m.end_date}",
                f"{m.days_present}/{m.days_expected}",
                f"{m.total_clicks:,}",
                f"{m.total_impressions:,}",
                f"{m.ctr:.2%}",
                pos_str,
            )

        console.print(table)

        # Performance Changes
        if result.click_change_percent is not None and result.impression_change_percent is not None:
            console.print("\n[bold]Metrics Delta (ROLLOUT vs PRE):[/bold]")
            c_color = "green" if result.click_change_percent >= 0 else "red"
            i_color = "green" if result.impression_change_percent >= 0 else "red"
            console.print(f"• Click Change: [{c_color}]{result.click_change_percent:+.2f}%[/{c_color}]")
            console.print(f"• Impression Change: [{i_color}]{result.impression_change_percent:+.2f}%[/{i_color}]")
            if result.ctr_change_points is not None:
                console.print(f"• CTR Delta: {result.ctr_change_points:+.2f} percentage points")

    # Technical Audit Status
    if result.technical_audit:
        tech = result.technical_audit
        t_status = "[bold red]FAIL - Blocking Issues Detected[/bold red]" if tech.has_blocking_issues else "[bold green]PASS - No Blocking Issues[/bold green]"
        console.print(f"\nTechnical Health Status: {t_status}")
        if tech.has_blocking_issues:
            console.print(f"• HTTP Errors: {tech.http_errors_count}")
            console.print(f"• Noindex Flagged: {tech.noindex_detected}")
            console.print(f"• Robots.txt Disallowed: {tech.robots_disallowed}")
            console.print(f"• Canonical Conflicts: {tech.canonical_issues_count}")
            console.print(f"• Redirect Issues: {tech.redirect_issues_count}")
            console.print(f"• SSR / Rendering Issues: {tech.ssr_issues_count}")

    # Position note
    if result.position_interpretation_note:
        console.print(f"\n[italic cyan]Note on Position:[/italic cyan] [dim]{result.position_interpretation_note}[/dim]")

    # Warnings
    if result.validation_warnings:
        console.print("\n[bold yellow]Warnings & Caveats:[/bold yellow]")
        for w in result.validation_warnings:
            console.print(f"  ⚠ {w}")

    # Disclaimer
    console.print(Panel(result.disclaimer, title="Scientific & Methodological Notice", style="dim"))

    # Save output if requested
    if output:
        out_p = Path(output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(result.model_dump_json(indent=2), encoding="utf-8")
        console.print(f"\n[bold green]Report saved to:[/bold green] {out_p}")
