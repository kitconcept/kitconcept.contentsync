from kitconcept.contentsync.utils import dotted_name_for_object

import typer


app = typer.Typer()


@app.command(name="info")
def tool_information():
    """Return information about the tool."""
    from kitconcept.contentsync import PACKAGE_NAME
    from kitconcept.contentsync import __version__
    from kitconcept.contentsync.settings import get_settings

    typer.echo(f"{PACKAGE_NAME}: {__version__}")
    settings = get_settings()
    typer.echo(f"- Sync Class: {dotted_name_for_object(settings.sync)}")
    typer.echo(f"- Source: {settings.src}")
    typer.echo(f"- Destination: {settings.dst}")
    typer.echo(f"- Destination (Base folder): {settings.base_dst_folder}")
    typer.echo(f"- Debug: {settings.debug}")
