from abc import ABC, abstractmethod


class Format(ABC):
    def __init__(self, data: dict, cols: list):
        self._data = data
        self._cols = cols

    @abstractmethod
    def echo(self):
        """ This method should be implemented. """
