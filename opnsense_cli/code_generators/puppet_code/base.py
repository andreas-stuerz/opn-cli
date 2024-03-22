from opnsense_cli.code_generators.base import CodeGenerator
from opnsense_cli.code_generators.puppet_code.factories import PuppetCodeFragmentFactory
from typing import List


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
        self._ignore_params = ["output", "cols", "help"]

    def _get_code_fragment(self, template_variable_name: str) -> List[str]:
        template_variable_name_namevar = f"{template_variable_name}_namevar"

        code_fragments = []

        for param_line in self._create_command_params:
            if param_line["name"] in self._ignore_params:
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

            code_fragments.append(code_type.get_code_fragment(getattr(code_type, template)))

        return code_fragments

    def _is_namevar(self, param_line):
        return param_line["name"] == self._find_uuid_by_column

    def _get_all_columns(self):
        columns = []
        for param_line in self._create_command_params:
            if param_line["name"] in self._ignore_params:
                continue
            columns.append(param_line["name"])
        return columns
