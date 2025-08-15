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


@app.command(name="dump", no_args_is_help=True)
def dump_contents(
    path: Annotated[Path, typer.Argument(help="Path to dump contents")],
    filter_key: Annotated[
        str, typer.Option(help="Filter the contents by its value. format: key=value")
    ] = "",
    transform: Annotated[
        bool, typer.Option(help="Whether to run the transform on each content")
    ] = False,
):
    """Connect to the source system, get the data and dump it to a local file."""
    folder = path.parent
    if not check_path(folder):
        typer.echo(f"Folder does not exist: {folder}")
        typer.Exit(1)
    dst = path.resolve()
    settings = get_settings()
    typer.echo(f"Dumping contents from {settings.src} to {dst}")
    syncer: ContentSyncer = settings.sync(
        item_converter=settings.item_converter,
        src_client=settings.src,
        dst_client=settings.dst,
        base_dst_folder=settings.base_dst_folder,
    )
    query = {}
    if filter_key:
        key, value = filter_key.split("=", 1)
        query[key] = value
    result = syncer.dump_contents(
        query=query,
        transform=transform,
    )
    with open(dst, "w") as fout:
        json.dump(result, fout, indent=2)
    typer.echo(f"- Contents were dumped successfully to {dst}")
