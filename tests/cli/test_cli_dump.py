from collections.abc import Generator
from kitconcept.contentsync.cli import app
from pathlib import Path
from typer.testing import CliRunner

import json
import pytest


runner = CliRunner()


@pytest.fixture
def dump_file(test_dir) -> Generator[Path, None, None]:
    filename = "output.json"
    path = test_dir / filename
    path.unlink(missing_ok=True)
    yield path
    path.unlink(missing_ok=True)


def test_cli_dump(start_containers, dump_file):
    result = runner.invoke(app, ["dump", "output.json"])
    assert result.exit_code == 0
    assert "Dumping contents from" in result.stdout
    assert dump_file.exists()
    data = json.loads(dump_file.read_text())
    assert isinstance(data, dict)
    assert len(data) == 4


@pytest.mark.parametrize(
    "filter_key,transform,expected_count",
    (
        ("username=dtremea", False, 1),
        ("username=dtremea", True, 1),
    ),
)
def test_cli_dump_with_filter(
    start_containers, dump_file, filter_key: str, transform: bool, expected_count: int
):
    transform_param = "--transform" if transform else "--no-transform"
    params = ["dump", f"{dump_file}", "--filter-key", filter_key, transform_param]
    result = runner.invoke(app, params)
    assert result.exit_code == 0
    data = json.loads(dump_file.read_text())
    assert len(data) == expected_count
