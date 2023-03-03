from opnsense_cli.dataclasses.code_generator.puppet.template_vars import PuppetTypeTemplateVars
from opnsense_cli.facades.code_generator.base import PuppetCodeGenerator
from opnsense_cli.facades.template_engines.base import TemplateEngine
from opnsense_cli.factories.base import ObjectTypeFromDataFactory


class PuppetTypeCodeGenerator(PuppetCodeGenerator):
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
        return f"opnsense_{self._click_group}_{self._click_command}.rb"

    def _get_template_vars(self):
        return PuppetTypeTemplateVars(
            click_command=self._click_command,
            click_group=self._click_group,
            find_uuid_by_column=self._find_uuid_by_column,
            examples=self._get_code_fragment('TEMPLATE_TYPE_example'),
            attributes=self._get_code_fragment('TEMPLATE_TYPE_attributes')
        )
