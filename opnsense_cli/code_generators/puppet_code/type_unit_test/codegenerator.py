from opnsense_cli.code_generators.puppet_code.type_unit_test.template_vars import PuppetTypeUnitTestTemplateVars
from opnsense_cli.code_generators.puppet_code.base import PuppetCodeGenerator
from opnsense_cli.template_engines.base import TemplateEngine
from opnsense_cli.code_generators.puppet_code.factories import PuppetCodeFragmentFactory


class PuppetTypeUnitTestCodeGenerator(PuppetCodeGenerator):
    def __init__(
        self,
        template_engine: TemplateEngine,
        type_factory: PuppetCodeFragmentFactory,
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
        return PuppetTypeUnitTestTemplateVars(
            click_command=self._click_command,
            click_group=self._click_group,
            find_uuid_by_column=self._find_uuid_by_column,
            new_resource=self._get_code_fragment("TEMPLATE_TYPE_UNIT_TEST_new_resource"),
            accepts_parameter=self._get_code_fragment("TEMPLATE_TYPE_UNIT_TEST_accepts_parameter"),
        )
