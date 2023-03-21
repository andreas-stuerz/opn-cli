from dataclasses import dataclass
from typing import List


@dataclass
class PuppetTypeTemplateVars:
    click_command: str
    click_group: str
    find_uuid_by_column: str
    examples: List[str]
    attributes: List[str]
