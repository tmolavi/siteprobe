import typer
from siteprobe import __version__
from siteprobe.cli.audit import audit_command
from siteprobe.cli.fix import fix_command
from siteprobe.cli.verify import verify_command
from siteprobe.cli.doctor import run_doctor
from siteprobe.cli.integrations import run_integrations
from siteprobe.mcp.server import run_mcp

app = typer.Typer(
    name="siteprobe",
    help="Open-source autonomous website auditor & fixer for SEO, GEO, performance, accessibility and technical web quality.",
    no_args_is_help=True,
)

app.command(name="audit", help="Run comprehensive public website audit")(audit_command)
app.command(name="fix", help="Execute safe, deterministic code remediations")(fix_command)
app.command(name="verify", help="Verify applied fixes and re-evaluate findings")(verify_command)
app.command(name="doctor", help="Inspect local environment capabilities and dependencies")(run_doctor)
app.command(name="integrations", help="List external provider integrations and connection status")(run_integrations)
app.command(name="serve-mcp", help="Launch Model Context Protocol (MCP) server over stdio")(run_mcp)


@app.callback(invoke_without_command=True)
def version_callback(
    version: bool = typer.Option(False, "--version", "-v", help="Show the SiteProbe version and exit")
):
    if version:
        typer.echo(f"SiteProbe version: {__version__}")
        raise typer.Exit()


if __name__ == "__main__":
    app()
