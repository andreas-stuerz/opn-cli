from dataclasses import dataclass


@dataclass
class OpnsenseApiTemplateVars:
    module_name: str
    controllers: dict
