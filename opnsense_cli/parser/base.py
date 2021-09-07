from abc import ABC, abstractmethod


class Parser(ABC):
    @abstractmethod
    def _set_content(self):
        """ This method should be implemented. """

    @abstractmethod
    def _parse_content(self) -> dict:
        """ This method should be implemented. """

    def parse(self):
        self._set_content()
        return self._parse_content()
