from abc import ABC, abstractmethod


class FormatFactory(ABC):
    def __init__(self, format_name):
        self._format_name = format_name

    @property
    @abstractmethod
    def _format_map(self) -> dict:
        """ This property should be implemented. """

    def get_formatter(self):
        return self._format_map.get(self._format_name, None)


class TypeFactory(ABC):
    @abstractmethod
    def get_type_for_data(self, data):
        """" This property should be implemented. """
