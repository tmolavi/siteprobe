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
    console.print("\n[dim]Core crawler, audit checks, i18n, and remediation work without any optional integrations.[/dim]\n")
