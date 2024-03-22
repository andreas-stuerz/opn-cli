from dataclasses import dataclass
from typing import List


@dataclass
class PuppetProviderUnitTestTemplateVars:
    click_command: str
    click_group: str
    find_uuid_by_column: str
    json: List[str]
    ruby_hash: List[str]
