from abc import ABC, abstractmethod

class CodeGenerator(ABC):
    @abstractmethod
    def generate_code(self):
        """ This method should be implemented. """
