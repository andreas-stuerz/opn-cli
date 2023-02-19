from dataclasses import dataclass


@dataclass
class PuppetProviderTemplateVars:
    click_command: str
    click_group: str

