from abc import ABC, abstractmethod


class Formatter(ABC):
    @abstractmethod
    def echo(self):
        """ This method should be implemented. """
