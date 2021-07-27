import click
from prettytable import PrettyTable
from opnsense_cli.formats.base import Format


class TableOutputFormat(Format):
    def echo(self):
        pretty_table = PrettyTable()
        pretty_table.field_names = self._cols
        json_type = self.get_json_type()
        filtered_data = json_type.get_filtered_by_columns(self._cols)

        for row in filtered_data:
            pretty_table.add_row(row)

        click.echo(pretty_table)
