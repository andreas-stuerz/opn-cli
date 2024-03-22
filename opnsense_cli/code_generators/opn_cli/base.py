from bs4 import Tag

from opnsense_cli.code_generators.base import CodeGenerator
from opnsense_cli.template_engines.base import TemplateEngine
from opnsense_cli.factories import ObjectTypeFromDataFactory


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
