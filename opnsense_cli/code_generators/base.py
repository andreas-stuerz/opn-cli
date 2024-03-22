import os
from abc import ABC, abstractmethod


class CodeGenerator(ABC):
    def write_code(self, path):
        code = self.get_code()
        return self._write_to_file(code, path)

    def _write_to_file(self, content, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as file:
            file.writelines(content)
        return f"generate new code: {path}"

    def _render_template(self, vars, template):
        self._template_engine.vars = vars
        self._template_engine.set_template_from_file(template)
        return self._template_engine.render()

    def get_code(self):
        template_vars = self._get_template_vars()
        return self._render_template(template_vars, self._template)

    @abstractmethod
    def _get_template_vars(self):
        """ " This method should be implemented."""
