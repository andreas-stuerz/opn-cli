from dataclasses import dataclass
from typing import List


@dataclass
class PuppetAcceptanceTestTemplateVars:
    click_command: str
    click_group: str
    find_uuid_by_column: str
    create_item: List[str]
    match_item: List[str]
    opn_cli_columns: List[str]
