from abc import ABC, abstractmethod
from dataclasses import dataclass
from opnsense_cli.exceptions.template_engine import TemplateEngineException


class TemplateEngine(ABC):
    def __init__(self, template_basedir):
        self.__vars = None
        self.__template = None
        self.template_basedir = template_basedir

    @property
    def template_basedir(self):
        return self.__template_basedir

    @template_basedir.setter
    def template_basedir(self, dir):
        self.__template_basedir = dir

    @property
    def template(self):
        if not self.__template:
            raise TemplateEngineException('missing template')
        return self.__template

    @template.setter
    def template(self, template):
        self.__template = template

    @property
    def vars(self):
        if not self.__vars:
            raise TemplateEngineException('missing template vars')
        return self.__vars

    @vars.setter
    def vars(self, template_var_obj: dataclass):
        self.__vars = template_var_obj

    @abstractmethod
    def set_template_from_string(self, template_str: str):
        """ This method should be implemented. """

    @abstractmethod
    def set_template_from_file(self, file):
        """ This method should be implemented. """

    @abstractmethod
    def render(self):
        """ This method should be implemented. """
