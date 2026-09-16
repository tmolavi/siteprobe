from typer.testing import CliRunner
from siteprobe import __version__
from siteprobe.cli.main import app

runner = CliRunner()


def test_cli_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_cli_doctor():
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "SiteProbe System Diagnostic" in result.output


def test_cli_integrations():
    result = runner.invoke(app, ["integrations"])
    assert result.exit_code == 0
    assert "SiteProbe External Integrations" in result.output
