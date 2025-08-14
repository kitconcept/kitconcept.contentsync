from kitconcept.contentsync.cli import app
from typer.testing import CliRunner

import json
import pytest


runner = CliRunner()


def test_cli_dump(start_containers, test_dir):
    result = runner.invoke(app, ["dump", "output.json"])
    assert result.exit_code == 0
    assert "Dumping contents from" in result.stdout
    assert (test_dir / "output.json").exists()
    data = json.loads((test_dir / "output.json").read_text())
    assert isinstance(data, dict)
    assert len(data) == 4


@pytest.mark.parametrize(
    "filter_key,transform,expected_count",
    (
        ("username=dtremea", False, 1),
        ("id=dtremea", True, 1),
    ),
)
def test_cli_dump_with_filter(
    start_containers, test_dir, filter_key: str, transform: bool, expected_count: int
):
    transform_param = "--transform" if transform else "--no-transform"
    params = ["dump", "output.json", "--filter-key", filter_key, transform_param]
    result = runner.invoke(app, params)
    assert result.exit_code == 0
    data = json.loads((test_dir / "output.json").read_text())
    assert len(data) == expected_count
