import os
from opnsense_cli.template_engines.base import TemplateEngine
from opnsense_cli.code_generators.base import CodeGenerator
from opnsense_cli.code_generators.opnsense_api.template_vars import OpnsenseApiTemplateVars


class OpnsenseApiCodeGenerator(CodeGenerator):
    def __init__(self, template_engine: TemplateEngine, template, controllers, module_name):
        self._template_engine = template_engine
        self._template = template
        self._controllers = controllers
        self._module_name = module_name

    def _get_template_vars(self):
        return OpnsenseApiTemplateVars(module_name=self._module_name, controllers=self._controllers)

    def _render_template(self, vars, template):
        self._template_engine.vars = vars
        self._template_engine.set_template_from_file(template)
        return self._template_engine.render()

    def get_code(self):
        vars = self._get_template_vars()
        return self._render_template(vars, self._template)

    def _write_to_file(self, content, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as file:
            file.writelines(content)
        return f"generate new code: {path}"
