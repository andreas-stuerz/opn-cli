import os
from abc import ABC, abstractmethod
from typing import List

from opnsense_cli.factories.base import ObjectTypeFromDataFactory
from opnsense_cli.facades.template_engines.base import TemplateEngine
from bs4.element import Tag

from opnsense_cli.factories.code_generator.puppet_code_fragment import PuppetCodeFragmentFactory


class CodeGenerator(ABC):
    def write_code(self, output_dir):
        code = self.get_code()
        filename = self._get_filename()
        path = os.path.join(output_dir, f"{filename}")
        return self._write_to_file(code, path)

    @abstractmethod
    def _get_filename(self):
        """ This method should be implemented. """

    def _write_to_file(self, content, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as file:
            file.writelines(content)
        return f"generate new code: {path}"

    def _render_template(self, vars, template):
        self._template_engine.vars = vars
        self._template_engine.set_template_from_file(template)
        return self._template_engine.render()

    def get_code(self):
        template_vars = self._get_template_vars()
        return self._render_template(template_vars, self._template)

    @abstractmethod
    def _get_template_vars(self):
        """" This method should be implemented. """


class PuppetCodeGenerator(CodeGenerator):
    def __init__(
            self,
            create_command_params,
            type_factory: PuppetCodeFragmentFactory,
            find_uuid_by_column,
            click_group,
            click_command,
    ):
        self._create_command_params = create_command_params
        self._type_factory = type_factory
        self._find_uuid_by_column = find_uuid_by_column
        self._click_group = click_group
        self._click_command = click_command
        self._ignore_params = ['output', 'cols', 'help']

    def _get_code_fragment(self, template_variable_name: str) -> List[str]:
        template_variable_name_namevar = f"{template_variable_name}_namevar"

        code_fragments = []

        for param_line in self._create_command_params:
            if param_line['name'] in self._ignore_params:
                continue

            code_type = self._type_factory.get_type_for_data(
                param_line,
                self._find_uuid_by_column,
                self._click_group,
                self._click_command,
            )

            template = template_variable_name
            if self._is_namevar(param_line) and hasattr(code_type, template_variable_name_namevar):
                template = template_variable_name_namevar

            code_fragments.append(
                code_type.get_code_fragment(getattr(code_type, template))
            )

        return code_fragments

    def _is_namevar(self, param_line):
        return param_line['name'] == self._find_uuid_by_column

    def _get_all_columns(self):
        columns = []
        for param_line in self._create_command_params:
            if param_line['name'] in self._ignore_params:
                continue
            columns.append(param_line['name'])
        return columns


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

    def _get_filename(self):
        return f"{self._click_command}.py"
