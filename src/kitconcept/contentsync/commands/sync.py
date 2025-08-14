from kitconcept.contentsync.settings import get_settings
from kitconcept.contentsync.sync import ContentSyncer

import typer


app = typer.Typer()


@app.command(name="sync")
def sync_contents():
    """Sync contents."""
    settings = get_settings()
    typer.echo(f"Syncing contents from {settings.src} to {settings.dst}")
    syncer: ContentSyncer = settings.sync(
        item_converter=settings.item_converter,
        src_client=settings.src,
        dst_client=settings.dst,
        base_dst_folder=settings.base_dst_folder,
    )
    report = syncer()
    typer.echo("Sync report")
    typer.echo(f"- Total source items: {report.total_src_items}")
    typer.echo(f"- Created items: {report.created_items}")
    typer.echo(f"- Updated items: {report.updated_items}")
    typer.echo(f"- Deleted items: {report.deleted_items}")
    if report.errors:
        typer.echo("Errors occurred during sync:")
        for error in report.errors:
            typer.echo(f" - {error}")
