from kitconcept.contentsync.cli import app
from typer.testing import CliRunner


runner = CliRunner()


def test_cli_dump(start_containers, test_dir):
    result = runner.invoke(app, ["dump", "output.json"])
    assert result.exit_code == 0
    assert "Dumping contents from" in result.stdout
    assert (test_dir / "output.json").exists()
