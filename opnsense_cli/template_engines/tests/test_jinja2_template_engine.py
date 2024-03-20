from opnsense_cli.tests.base import BaseTestCase
from opnsense_cli.template_engines.jinja2 import Jinja2TemplateEngine
from opnsense_cli.template_engines.exceptions import TemplateEngineException, TemplateNotFoundException
from opnsense_cli.template_engines.tests.fixtures.template_vars import TemplateTestVars


class Test_Jinja2TemplateEngine(BaseTestCase):
    def setUp(self):
        self._template_basedir = self._get_fixture_path("", "../fixtures/tests/template_engines")
        self._engine = Jinja2TemplateEngine(self._template_basedir)

    def test_template_render_OK(self):
        self._engine.set_template_from_string("My name: {{ vars.my_name }}")
        self._engine.vars = TemplateTestVars(my_name="opn-cli")
        result = self._engine.render()
        self.assertIn("My name: opn-cli", result)

    def test_template_not_found_ERROR(self):
        self.assertRaises(TemplateNotFoundException, self._engine.set_template_from_file, "does_not_exists.py.j2")

    def test_template_missing_ERROR(self):
        self.assertRaises(TemplateEngineException, self._engine.render)

    def test_template_vars_missing_ERROR(self):
        self._engine.set_template_from_string("a jinja template")
        self.assertRaises(TemplateEngineException, self._engine.render)
