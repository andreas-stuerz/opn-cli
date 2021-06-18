import click
from opnsense_cli.formats.base import Format
from abc import ABC, abstractmethod


class TableInputFormat(ABC):
    def __init__(self, input_data: dict, filter_columns: list):
        self._input_data = input_data
        self._filter_columns = filter_columns

    @abstractmethod
    def get_filtered_by_columns(self) -> list:
        result = []
        for item in self._input_data:
            row = [value for name, value in item.items()]
            if self._filter_columns:
                row = [str(item[column]) for column in self._filter_columns]
            result.append(row)
        return result

class JsonObjList(TableInputFormat):
    """
    Transform array of json objects
    Example:
    [
        {"name": "obj1"},
        {"name", "obj2"}
    ]
    """
    def get_filtered_by_columns(self):
        return super().get_filtered_by_columns()


class JsonObjNested(TableInputFormat):
    """
    Table Output for nested json Objects.
    Example:
    {
        '567f2891c6002': {'description': 'vpn name 1', 'users': []},
        '567f28af0cb4d': {'description': 'vpn name 2', 'users': []}
    }
    """
    def __init__(self, input_data: dict, filter_columns: list):
        self._input_data = self.extract_id_column(input_data)
        self._filter_columns = filter_columns

    def extract_id_column(self, input_data):
        """
        Extract the key of each json row and add it in each json obj with attribute name <ID>
        """
        result = []
        for item in input_data:
            line = {}
            line.update({
                '<ID>': item
            })
            line.update(input_data[item])
            result.append(line)
        return result

    def get_filtered_by_columns(self):
        return super().get_filtered_by_columns()


class TableFormat(Format):
    """
    Output a human readable table
    """

    def __init__(self, data: dict, cols: list):
        super().__init__(data, cols)
        self._separator = " "

    @property
    def separator(self):
        return self._separator

    @separator.setter
    def separator(self, value):
        self._separator = value

    def get_input_format(self):
        if isinstance(self._data, list):
            return JsonObjList(self._data, self._cols)

        if isinstance(self._data, dict):
            for key, val in self._data.items():
                if not isinstance(val, dict):
                    self._data = [self._data]
                    return JsonObjList(self._data, self._cols)
            return JsonObjNested(self._data, self._cols)

        raise NotImplementedError("Type of JSON Input is unknown.")

    def echo(self):
        input_format = self.get_input_format()
        filtered_data = input_format.get_filtered_by_columns()
        for row in filtered_data:
            click.echo(self.separator.join(row))


