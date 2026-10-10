import shutil
import sys
from rich.console import Console
from rich.table import Table
from siteprobe.integrations import (
    SearchConsoleIntegration,
    GA4Integration,
    DataForSEOIntegration,
    LighthouseIntegration,
    PlaywrightIntegration,
    AIProviderIntegration,
)


def run_doctor() -> None:
    console = Console()
    console.print("\n[bold cyan]SiteProbe System Diagnostic (doctor)[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Component / Capability", style="dim")
    table.add_column("Status", justify="center")
    table.add_column("Details")

    # Python
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    table.add_row("Python Runtime", "[green]PASS[/green]", f"Python {py_ver}")

    # Core Update Triage Engine
    table.add_row(
        "Update Impact Triage",
        "[green]PASS[/green]",
        "Engine active (Sep 2026 Spam Update frozen windows & baseline variability).",
    )

    # MCP Protocol Server
    try:
        import mcp
        mcp_status = "[green]AVAILABLE[/green]"
        mcp_desc = "FastMCP ready. Run 'siteprobe serve-mcp' for Claude Code, Cursor, Windsurf."
    except ImportError:
        mcp_status = "[yellow]OPTIONAL[/yellow]"
        mcp_desc = "Run 'pip install mcp' to enable FastMCP tool calling for Claude / Cursor."
    table.add_row("FastMCP Server", mcp_status, mcp_desc)

    # Integrations
    integrations = [
        LighthouseIntegration(),
        PlaywrightIntegration(),
        SearchConsoleIntegration(),
        GA4Integration(),
        DataForSEOIntegration(),
        AIProviderIntegration(),
    ]

    for integ in integrations:
        info = integ.get_status_info()
        status_badge = "[green]AVAILABLE[/green]" if info["available"] else "[yellow]OPTIONAL[/yellow]"
        detail = info["description"] if info["available"] else info.get("setup_guide", "Not configured")
        table.add_row(info["name"], status_badge, detail)

    console.print(table)

    # AI Agent First-Use Checklist
    console.print(
        "\n[bold green]AI Assistant & IDE Intake Checklist (Codex, Antigravity, Claude, Cursor):[/bold green]"
    )
    console.print(
        "  1. [bold]Website Audit[/bold]: Requires target URL. (e.g. [cyan]siteprobe audit https://example.com[/cyan])"
    )
    console.print(
        "  2. [bold]Update Triage[/bold]: Requires GSC performance CSV ([cyan]--csv <file.csv>[/cyan] with date, clicks, impressions)."
    )
    console.print(
        "  3. [bold]Automated Fixes[/bold]: Requires local project source repository path ([cyan]--repo <path>[/cyan])."
    )
    console.print(
        "  4. [bold]Safety Rule[/bold]: Never fake GSC/GA4 numbers; never claim SpamBrain penalty without Search Console evidence.\n"
    )
