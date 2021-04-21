from opnsense_cli.command import format


class CliOutput():
    formatter_map = {
        'json': format.JsonFormat,
        'table': format.TableFormat
    }

    def __init__(self, data, format_name, cols=None):
        self._data = data
        self._format_name = format_name
        self._cols = cols

    def get_formatter(self):
        output_class = self.formatter_map.get(self._format_name, None)
        return output_class(self._data, self._cols)

    def echo(self):
        self.get_formatter().echo()
