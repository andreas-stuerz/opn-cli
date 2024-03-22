import json
from abc import ABC, abstractmethod
import click
import yaml
from prettytable import PrettyTable
from opnsense_cli.formatters.cli_output.json_type_factory import JsonTypeFactory


class Format(ABC):
    def __init__(self, json_data: dict, cols: list, json_type_factory=JsonTypeFactory()):
        self._json_data = json_data
        self._json_type_factory = json_type_factory
        self._cols = self.get_all_cols() if cols == [""] else cols

    def get_all_cols(self):
        json_type = self.get_json_type()
        return json_type.get_all_columns()

    def get_json_type(self):
        return self._json_type_factory.get_type_for_data(self._json_data)

    def get_filtered_data_by_columns(self):
        json_type = self.get_json_type()
        filtered_data = json_type.get_filtered_by_columns(self._cols)

        if len(filtered_data) > 1:
            return self._get_filtered_data_for_list(filtered_data)

        return self._get_filtered_data_for_obj(filtered_data)

    def _get_filtered_data_for_obj(self, line: list):
        if not line:
            return {}
        return dict(zip(self._cols, line[0]))

    def _get_filtered_data_for_list(self, lines: list):
        result = []
        for line in lines:
            result.append(dict(zip(self._cols, line)))
        return result

    @abstractmethod
    def echo(self):
        """This method should be implemented."""


class ColsOutputFormat(Format):
    def echo(self):
        click.echo(",".join(self._cols))


class JsonFilterOutputFormat(Format):
    def echo(self):
        filtered_data = self.get_filtered_data_by_columns()
        click.echo(json.dumps(filtered_data))


class JsonOutputFormat(Format):
    def echo(self):
        click.echo(json.dumps(self._json_data))


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


class TableOutputFormat(Format):
    def echo(self):
        pretty_table = PrettyTable()
        pretty_table.field_names = self._cols
        json_type = self.get_json_type()
        filtered_data = json_type.get_filtered_by_columns(self._cols)

        for row in filtered_data:
            pretty_table.add_row(row)

        click.echo(pretty_table)


class YamlOutputFormat(Format):
    def echo(self):
        filtered_data = self.get_filtered_data_by_columns()
        yaml_output = yaml.dump(filtered_data, sort_keys=False)
        click.echo(yaml_output)
