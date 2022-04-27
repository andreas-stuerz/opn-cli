from dataclasses import dataclass


@dataclass
class ApiTemplateVars:
    module_name: str
    controllers: dict
