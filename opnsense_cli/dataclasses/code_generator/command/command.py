from dataclasses import dataclass


@dataclass
class CommandTemplateVars:
    click_command: str
    click_group: str
    click_options_create: list
    click_options_update: list
    column_names: list
    column_list: str
    module_type: str
