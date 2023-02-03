import click

from opnsense_cli import __cli_name__, __version__


@click.command()
def version():
    """
    Show the CLI version and exit.
    """
    click.echo(f"{__cli_name__} v{__version__}")
