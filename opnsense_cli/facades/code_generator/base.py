import os
from abc import ABC, abstractmethod
from opnsense_cli.factories.base import ObjectTypeFromDataFactory
from opnsense_cli.facades.template_engines.base import TemplateEngine
from bs4.element import Tag


class CodeGenerator(ABC):
    def write_code(self, output_dir):
        """" This method should be implemented. """

    def get_code(self):
        """" This method should be implemented. """


class CommandCodeGenerator(CodeGenerator):
    def __init__(
            self,
            tag_content: Tag,
            template_engine: TemplateEngine,
            option_factory: ObjectTypeFromDataFactory,
            template,
            group,
            command,
            model_xml_tag,
            module_type,
    ):
        self._tag_content: Tag = tag_content
        self._template_engine = template_engine
        self._template = template
        self._click_group = group
        self._click_command = command
        self._click_option_factory = option_factory
        self._model_xml_tag = model_xml_tag
        self._module_type = module_type

    def write_code(self, output_dir, filename_prefix='', filename_suffix='.py'):
        code = self.get_code()
        filename = f"{filename_prefix}{self._click_command}{filename_suffix}"
        path = os.path.join(output_dir, f"{filename}")
        return self._write_to_file(code, path)

    def get_code(self):
        template_vars = self._get_template_vars()
        return self._render_template(template_vars, self._template)

    @abstractmethod
    def _get_template_vars(self):
        """" This method should be implemented. """

    def _render_template(self, vars, template):
        self._template_engine.vars = vars
        self._template_engine.set_template_from_file(template)
        return self._template_engine.render()

    def _write_to_file(self, content, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as file:
            file.writelines(content)
        return f"generate new code: {path}"
