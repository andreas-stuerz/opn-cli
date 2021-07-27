import click
from opnsense_cli.formats.base import Format


class PlainOutputFormat(Format):
    def __init__(self, json_data: dict, cols: list):
        super().__init__(json_data, cols)
        self._separator = " "

    @property
    def separator(self):
        return self._separator

    @separator.setter
    def separator(self, value):
        self._separator = value

    def echo(self):
        json_type = self.get_json_type()
        filtered_data = json_type.get_filtered_by_columns(self._cols)

        for row in filtered_data:
            click.echo(self.separator.join(row))
