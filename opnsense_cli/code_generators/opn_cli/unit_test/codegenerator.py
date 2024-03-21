from opnsense_cli.code_generators.opn_cli.base import CommandCodeGenerator
from opnsense_cli.code_generators.opn_cli.unit_test.template_vars import CommandTestTemplateVars


class ClickCommandTestCodeGenerator(CommandCodeGenerator):

    def _get_template_vars(self):
        return CommandTestTemplateVars(
            click_command=self._click_command,
            click_group=self._click_group,
            model_xml_tag=self._model_xml_tag,
            module_type=self._module_type,
        )
