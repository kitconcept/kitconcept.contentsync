from kitconcept.contentsync import __version__
from kitconcept.contentsync.cli import app
from typer.testing import CliRunner


runner = CliRunner()


def test_cli_info_version():
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert f"kitconcept.contentsync: {__version__}" in result.stdout
