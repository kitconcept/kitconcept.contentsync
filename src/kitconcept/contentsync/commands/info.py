from kitconcept.contentsync import utils
from kitconcept.contentsync.clients import ConnectionClient
from typing import Annotated

import typer


app = typer.Typer()


SUPPRESSED_LOGGERS = ["kitconcept.contentsync", "urllib3.connectionpool"]


def _do_connect(name: str, client: ConnectionClient):
    """Test connection to a client system."""
    with utils.suppress_logging(SUPPRESSED_LOGGERS):
        status = client.test_connection()
    status_str = "✅" if status else "❗"
    typer.echo(f"  - {name}: {status_str}")


@app.command(name="info")
def tool_information(
    test_connection: Annotated[
        bool, typer.Option(help="Should we test the connection to remote systems?")
    ] = False,
):
    """Return information about the tool."""
    from kitconcept.contentsync import PACKAGE_NAME
    from kitconcept.contentsync import __version__
    from kitconcept.contentsync.settings import get_settings

    typer.echo(f"{PACKAGE_NAME}: {__version__}")
    settings = get_settings()
    typer.echo(f"- Sync Class: {utils.dotted_name_for_class(settings.sync)}")
    typer.echo(f"- Source: {settings.src}")
    typer.echo(f"- Destination: {settings.dst}")
    typer.echo(f"- Destination (Base folder): {settings.base_dst_folder}")
    typer.echo(f"- Debug: {settings.debug}")
    if test_connection:
        typer.echo("- Connections")
        _do_connect("Source", settings.src)
        _do_connect("Destination", settings.src)
