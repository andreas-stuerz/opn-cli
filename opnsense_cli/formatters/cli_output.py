from opnsense_cli.formatters.base import Formatter
from opnsense_cli.formats.base import Format


class CliOutputFormatter(Formatter):
    def __init__(self, data, format: Format, cols=None):
        self._data = data
        self._format = format
        self._cols = cols

    def echo(self):
        format: Format = self._format(self._data, self._cols)
        format.echo()
