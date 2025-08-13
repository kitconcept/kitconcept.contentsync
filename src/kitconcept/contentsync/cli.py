from kitconcept.contentsync.commands.dump import app as app_dumper
from kitconcept.contentsync.commands.info import app as app_info
from kitconcept.contentsync.commands.sync import app as app_sync

import typer


app = typer.Typer(no_args_is_help=True)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Welcome to kitconcept.contentsync."""
    pass


app.add_typer(app_dumper)
app.add_typer(app_info)
app.add_typer(app_sync)


def cli():
    app()


__all__ = ["cli"]
