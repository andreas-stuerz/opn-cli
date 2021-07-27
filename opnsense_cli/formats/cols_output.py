import click
from opnsense_cli.formats.base import Format


class ColsOutputFormat(Format):
    def echo(self):
        click.echo(",".join(self._cols))
