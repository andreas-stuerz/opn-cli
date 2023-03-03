from opnsense_cli.dataclasses.code_generator.puppet.provider_vars import PuppetProviderTemplateVars
from opnsense_cli.facades.code_generator.base import CodeGenerator
from opnsense_cli.facades.template_engines.base import TemplateEngine
from opnsense_cli.factories.base import ObjectTypeFromDataFactory


class PuppetProviderCodeGenerator(CodeGenerator):
    def __init__(
            self,
            template_engine: TemplateEngine,
            type_factory: ObjectTypeFromDataFactory,
            template,
            group,
            command,
            find_uuid_by_column,
            create_command_params,
            update_command_params,
    ):
        self._type_factory = type_factory
        self._template_engine = template_engine
        self._template = template
        self._click_group = group
        self._click_command = command
        self._find_uuid_by_column = find_uuid_by_column
        self._create_command_params = create_command_params
        self._update_command_params = update_command_params

    def _get_filename(self):
        return f"opnsense_{self._click_group}_{self._click_command}/opnsense_{self._click_group}_{self._click_command}.rb"

    def _get_template_vars(self):
        return PuppetProviderTemplateVars(
            click_command=self._click_command,
            click_group=self._click_group,
            find_uuid_by_column=self._find_uuid_by_column,
            translate_json_object_to_puppet_resource=self._get_translate_json_object_to_puppet_resource(),
            translate_puppet_resource_to_command_args=self._get_translate_puppet_resource_to_command_args(),
        )

    def _get_translate_json_object_to_puppet_resource(self):
        ignore_params = ['output', 'cols', 'help']
        code_fragments = []
        for param_line in self._create_command_params:
            if param_line['name'] in ignore_params:
                continue

            code_type = self._type_factory.get_type_for_data(param_line)

            code_fragments.append(
                code_type.get_code_fragment(
                    code_type.TEMPLATE_translate_json_object_to_puppet_resource
                )
            )

        return code_fragments

    def _get_translate_puppet_resource_to_command_args(self):
        ignore_params = ['output', 'cols', 'help']
        code_fragments = []
        for param_line in self._create_command_params:
            if param_line['name'] in ignore_params:
                continue

            code_type = self._type_factory.get_type_for_data(param_line)

            code_fragments.append(
                code_type.get_code_fragment(
                    code_type.TEMPLATE_translate_puppet_resource_to_command_args
                )
            )

        return code_fragments

