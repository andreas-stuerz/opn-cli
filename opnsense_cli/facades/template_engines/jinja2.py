import os
from jinja2 import Template, Environment, FileSystemLoader, BaseLoader
from opnsense_cli.facades.template_engines.base import TemplateEngine
from opnsense_cli.exceptions.template_engine import TemplateNotFoundException
from jinja2.exceptions import TemplateNotFound,TemplatesNotFound

class Jinja2TemplateEngine(TemplateEngine):
    def set_template_from_string(self, template_str, **kwargs) -> Template:
        self.template = Environment(loader=BaseLoader, **kwargs).from_string(template_str)

    def set_template_from_file(self, template, **kwargs) -> Template:
        env = Environment(loader = FileSystemLoader(self.template_basedir), **kwargs)
        try:
            self.template = env.get_template(template)
        except (TemplateNotFound,TemplatesNotFound) as e:
            basedir = os.path.abspath(self.template_basedir)
            template_path = os.path.join(basedir, template)
            raise TemplateNotFoundException(template_path)

    def render(self):
        return self.template.render(vars=self.vars)





