from dataclasses import dataclass


@dataclass
class FacadeTemplateVars:
    click_command: str
    click_group: str
    model_xml_tag: str
    resolver_map: list
    module_type: str


