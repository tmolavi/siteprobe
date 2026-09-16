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


def run_integrations() -> None:
    console = Console()
    console.print("\n[bold cyan]SiteProbe External Integrations & Providers[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Integration")
    table.add_column("Status", justify="center")
    table.add_column("Capabilities")
    table.add_column("Configuration")

    integrations = [
        SearchConsoleIntegration(),
        GA4Integration(),
        DataForSEOIntegration(),
        LighthouseIntegration(),
        PlaywrightIntegration(),
        AIProviderIntegration(),
    ]

    for integ in integrations:
        info = integ.get_status_info()
        status_badge = "[green]READY[/green]" if info["available"] else "[dim]NOT CONFIGURED[/dim]"
        table.add_row(info["name"], status_badge, info["description"], info.get("setup_guide", ""))

    console.print(table)
    console.print()
