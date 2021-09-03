from dataclasses import dataclass


@dataclass
class CommandFacadeTemplateVars:
    click_command: str
    click_group: str
    model_xml_tag: str
    resolver_map: dict
    module_type: str
