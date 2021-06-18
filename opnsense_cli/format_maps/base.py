from abc import ABC, abstractmethod
from opnsense_cli.formats.base import Format

class FormatterMap(ABC):
    def __init__(self, format_name):
        self._format_name = format_name

    @property
    @abstractmethod
    def _format_map(self) -> dict:
        """ This property should be implemented. """

    def get_formatter(self) -> Format:
        return self._format_map.get(self._format_name, None)
