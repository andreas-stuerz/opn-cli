import click
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
        click.echo(self._data)


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

    def echo(self):
        for item in self._data:
            cols = [value for name, value in item.items()]
            if self._cols:
                cols = [item[column] for column in self._cols]
            click.echo(self.separator.join(cols))
