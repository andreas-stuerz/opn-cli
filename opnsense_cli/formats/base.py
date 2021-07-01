from abc import ABC, abstractmethod
from opnsense_cli.factories.json_type import JsonTypeFactory


class Format(ABC):
    def __init__(self, json_data: dict, cols: list, json_type_factory=JsonTypeFactory()):
        self._json_data = json_data
        self._cols = cols
        self._json_type_factory = json_type_factory

    def get_json_type(self):
        return self._json_type_factory.get_type_for_data(self._json_data)

    @abstractmethod
    def echo(self):
        """ This method should be implemented. """
