from dataclasses import dataclass


@dataclass
class PuppetTypeTemplateVars:
    click_command: str
    click_group: str
    find_uuid_by_column: str
    examples: str
    attributes: str

