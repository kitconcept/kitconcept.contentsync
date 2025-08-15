from kitconcept.contentsync import __version__
from kitconcept.contentsync.cli import app
from typer.testing import CliRunner

import pytest


runner = CliRunner()


def test_cli_info_version():
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert f"kitconcept.contentsync: {__version__}" in result.stdout


@pytest.mark.parametrize(
    "flag,expected",
    [
        ["--test-connection", "- Connections"],
        ["--test-connection", "- Source: ✅"],
        ["--test-connection", "- Destination: ✅"],
    ],
)
def test_cli_info_connections(flag: str, expected: str):
    result = runner.invoke(app, ["info", flag])
    assert result.exit_code == 0
    assert expected in result.stdout
