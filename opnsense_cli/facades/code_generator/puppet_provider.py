from opnsense_cli.dataclasses.code_generator.puppet.provider_vars import PuppetProviderTemplateVars
from opnsense_cli.facades.code_generator.base import CommandCodeGenerator, CodeGenerator
from opnsense_cli.facades.template_engines.base import TemplateEngine
from opnsense_cli.types.click_option.base import ClickOptionCodeFragment
from opnsense_cli.dataclasses.code_generator.command.command_vars import CommandTemplateVars
import os

class PuppetProviderCodeGenerator(CodeGenerator):
    def __init__(
            self,
            template_engine: TemplateEngine,
            template,
            group,
            command,
    ):
        self._template_engine = template_engine
        self._template = template
        self._click_group = group
        self._click_command = command

    def _get_filename(self):
        return f"opnsense_{self._click_group}_{self._click_command}/opnsense_{self._click_group}_{self._click_command}.rb"

    def _get_template_vars(self):
        return PuppetProviderTemplateVars(
            click_command=self._click_command,
            click_group=self._click_group,
        )



