from opnsense_cli.code_generators.puppet_code.acceptance_test.template_vars import PuppetAcceptanceTestTemplateVars
from opnsense_cli.code_generators.puppet_code.base import PuppetCodeGenerator
from opnsense_cli.template_engines.base import TemplateEngine
from opnsense_cli.factories import ObjectTypeFromDataFactory


class PuppetAcceptanceTestCodeGenerator(PuppetCodeGenerator):
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
        super().__init__(create_command_params, type_factory, find_uuid_by_column, group, command)
        self._template_engine = template_engine
        self._template = template
        self._update_command_params = update_command_params


    def _get_template_vars(self):
        return PuppetAcceptanceTestTemplateVars(
            click_command=self._click_command,
            click_group=self._click_group,
            find_uuid_by_column=self._find_uuid_by_column,
            create_item=self._get_code_fragment("TEMPLATE_ACCEPTANCE_TEST_create_item"),
            match_item=self._get_code_fragment("TEMPLATE_ACCEPTANCE_TEST_match_item"),
            opn_cli_columns=self._get_all_columns(),
        )
