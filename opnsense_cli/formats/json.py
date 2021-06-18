import click
import json
from opnsense_cli.formats.base import Format


class JsonFormat(Format):
    def echo(self):
        click.echo(json.dumps(self._data))
