from dataclasses import dataclass


@dataclass
class PuppetTypeUnitTestTemplateVars:
    click_command: str
    click_group: str
    find_uuid_by_column: str
    new_resource: str
    accepts_parameter: str

