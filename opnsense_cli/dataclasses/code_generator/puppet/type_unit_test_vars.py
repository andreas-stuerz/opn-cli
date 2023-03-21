from dataclasses import dataclass
from typing import List


@dataclass
class PuppetTypeUnitTestTemplateVars:
    click_command: str
    click_group: str
    find_uuid_by_column: str
    new_resource: List[str]
    accepts_parameter: List[str]
