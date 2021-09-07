from abc import ABC, abstractmethod


class ClassFromKeymapFactory(ABC):
    def __init__(self, key):
        self._key = key

    @property
    @abstractmethod
    def _keymap(self) -> dict:
        """ This property should be implemented. """

    def get_class(self):
        return self._keymap.get(self._key, None)


class ObjectTypeFromDataFactory(ABC):
    @abstractmethod
    def get_type_for_data(self, data):
        """" This method should be implemented. """
