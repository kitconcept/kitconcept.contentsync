from kitconcept.contentsync.settings import get_settings
from kitconcept.contentsync.sync import ContentSyncer
from pathlib import Path
from typing import Annotated

import json
import typer


app = typer.Typer()


def check_path(path: Path) -> bool:
    """Check if path exists."""
    path = path.resolve()
    return path.exists()


@app.command(name="dump")
def dump_contents(
    dst: Annotated[Path, typer.Argument(help="Path to dump contents")],
):
    """Connect to the source system, get the data and dump it to a local file."""
    folder = dst.parent
    if not check_path(folder):
        typer.echo(f"Folder does not exist: {folder}")
        typer.Exit(1)
    dst = dst.resolve()
    settings = get_settings()
    typer.echo(f"Dumping contents from {settings.src} to {dst}")
    syncer: ContentSyncer = settings.sync(
        src_client=settings.src,
        dst_client=settings.dst,
        base_dst_folder=settings.base_dst_folder,
    )
    result = syncer.dump_contents(transform=False)
    with open(dst, "w") as fout:
        json.dump(result, fout, indent=2)
    typer.echo(f"- Contents were dumped successfully to {dst}")
