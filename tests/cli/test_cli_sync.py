from kitconcept.contentsync.cli import app
from typer.testing import CliRunner


runner = CliRunner()


def test_cli_sync(start_containers):
    result = runner.invoke(app, ["sync"])
    assert result.exit_code == 0
    assert "Sync report" in result.stdout
    assert "- Total source items: 4" in result.stdout
