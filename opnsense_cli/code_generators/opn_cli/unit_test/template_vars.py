from dataclasses import dataclass


@dataclass
class CommandTestTemplateVars:
    click_command: str
    click_group: str
    model_xml_tag: str
    module_type: str
