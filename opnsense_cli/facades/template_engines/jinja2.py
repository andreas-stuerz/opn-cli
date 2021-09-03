import os
from jinja2 import Template, Environment, BaseLoader
from opnsense_cli.facades.template_engines.base import TemplateEngine
from opnsense_cli.exceptions.template_engine import TemplateNotFoundException
from jinja2.exceptions import TemplateNotFound, TemplatesNotFound


class Jinja2TemplateEngine(TemplateEngine):
    def set_template_from_file(self, template, **kwargs):
        path = os.path.abspath(os.path.join(self.template_basedir, template))
        try:
            template_content = self._read_file(path)
            self.set_template_from_string(template_content)
        except (TemplateNotFound, TemplatesNotFound, FileNotFoundError):
            basedir = os.path.abspath(self.template_basedir)
            template_path = os.path.join(basedir, template)
            raise TemplateNotFoundException(template_path)

    def set_template_from_string(self, template_str, **kwargs) -> Template:
        self.template = Environment(loader=BaseLoader, **kwargs).from_string(template_str)

    def render(self):
        return self.template.render(vars=self.vars)

    def _read_file(self, path):
        with open(path) as file:
            content = file.read()
        return content
