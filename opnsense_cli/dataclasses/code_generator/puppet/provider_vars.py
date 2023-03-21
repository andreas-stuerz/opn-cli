from dataclasses import dataclass
from typing import List


@dataclass
class PuppetProviderTemplateVars:
    click_command: str
    click_group: str
    find_uuid_by_column: str
    translate_json_object_to_puppet_resource: List[str]
    translate_puppet_resource_to_command_args: List[str]
