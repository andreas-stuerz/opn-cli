import click
import json
from abc import ABC, abstractmethod


class BaseFormat(ABC):
    """
    The base abstract class for command output formats
    """

    def __init__(self, data: dict, cols: list):
        self._data = data
        self._cols = cols

    @abstractmethod
    def echo(self):
        """ This method should be implemented. """


class JsonFormat(BaseFormat):
    """
    Outputs Json
    """

    def echo(self):
        click.echo(json.dumps(self._data))


class TableFormat(BaseFormat):
    """
    Output a human readable table
    """

    def __init__(self, data: dict, cols: list):
        super().__init__(data, cols)
        self._separator = " "

    @property
    def seperator(self):
        return self._separator

    @seperator.setter
    def separator(self, value):
        self._separator = value

    def print_json_obj_list(self):
        """
        Table Output for array of json Objects
        Example:
        [
            {"name": "obj1"},
            {"name", "obj2"}
        ]
        """
        for item in self._data:
            cols = [value for name, value in item.items()]
            if self._cols:
                cols = [str(item[column]) for column in self._cols]
            click.echo(self.separator.join(cols))

    def print_json_obj(self):
        """
        Table Output for json Objects.
        Example:
        {
            'description': 'vpn name 1', 'users': []
        }
        """

    def print_json_obj_nested(self):
        """
        Table Output for nested json Objects.
        Example:
        {
            '567f2891c6002': {'description': 'vpn name 1', 'users': []},
            '567f28af0cb4d': {'description': 'vpn name 2', 'users': []}
        }
        """
        data = []
        for item in self._data:
            line = {}
            line.update({
                '<ID>': item
            })
            line.update(self._data[item])
            data.append(line)

        self._data = data
        self.print_json_obj_list()

    def echo(self):
        if isinstance(self._data, list):
            return self.print_json_obj_list()

        if isinstance(self._data, dict):
            for key, val in self._data.items():
                if not isinstance(val, dict):
                    self._data = [self._data]
                    return self.print_json_obj_list()

            return self.print_json_obj_nested()

        raise NotImplementedError("Type of JSON Input is unknown.")
