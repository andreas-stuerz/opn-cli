from opnsense_cli.code_generators.opn_cli.base import CommandCodeGenerator
from opnsense_cli.code_generators.opn_cli.service.template_vars import CommandServiceTemplateVars
from bs4.element import Tag


class ClickCommandServiceCodeGenerator(CommandCodeGenerator):
    def _get_template_vars(self):
        resolver_map = {}
        for tag in self._tag_content.findChildren(recursive=False):
            resolver_item = self._get_resolver(tag)

            if resolver_item:
                resolver_map.update(resolver_item)

        return CommandServiceTemplateVars(
            click_command=self._click_command,
            click_group=self._click_group,
            model_xml_tag=self._model_xml_tag,
            resolver_map=resolver_map,
            module_type=self._module_type,
        )

    def _get_resolver(self, tag: Tag):
        if tag.attrs.get("type") != "ModelRelationField":
            return None

        items = tag.find("items").string
        template = f"$.{self._click_group}.{items}" + "[{uuids}]." f"{tag.find('display').string}"

        insert_as_key = items.split(".")[1].capitalize()
        if tag.find(name="Multiple", text="Y") or tag.find(name="multiple", text="Y"):
            insert_as_key = items.split(".")[0].capitalize()

        result = {tag.name: {"template": template, "insert_as_key": insert_as_key}}

        return result
