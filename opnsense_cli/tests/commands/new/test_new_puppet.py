import os
from unittest.mock import patch, Mock
from opnsense_cli.commands.new.puppet import puppet
from opnsense_cli.tests.commands.base import CommandTestCase
from click.testing import CliRunner
import textwrap


class TestNewPuppetCommands(CommandTestCase):
    def setUp(self):
        self._setup_fakefs()

        self._core_model_fixture = self._read_fixture_file('new/command/core/model.xml')
        self._core_form_fixture = self._read_fixture_file('new/command/core/form.xml')
        self._plugin_model_fixture = self._read_fixture_file('new/command/plugin/model.xml')
        self._plugin_form_fixture = self._read_fixture_file('new/command/plugin/form.xml')


        self._command_template = self._read_template_file('code_generator/command/command.py.j2')
        self._facade_template = self._read_template_file('code_generator/command/command_facade.py.j2')
        self._test_template = self._read_template_file('code_generator/command/command.py.j2')

        self._output_dir = self._get_output_path('')
        self._generated_provider_path = f"{self._output_dir}/puppet/provider/opnsense_haproxy_frontend/opnsense_haproxy_frontend.rb"
        self._generated_type_path = f"{self._output_dir}/puppet/type/opnsense_haproxy_frontend.rb"
        self._generated_provider_test_path = f"{self._output_dir}/puppet/spec/unit/puppet/type/opnsense_haproxy_frontend_spec.rb"
        self._generated_type_test_path = f"{self._output_dir}/puppet/spec/unit/puppet/provider/opnsense_haproxy_frontend_spec.rb"
        self._generated_acceptance_test_path = f"{self._output_dir}/puppet/spec/acceptance/types/opnsense_haproxy_frontend_spec.rb"


    def test_puppet_resource(self):
        runner = CliRunner()
        result = runner.invoke(
            puppet,
            [
                'resource-type', 'haproxy', 'frontend', 'name'
            ],
            catch_exceptions=True
        )

        self.assertIn(f"generate new code: {self._generated_provider_path}\n", result.output)
        self.assertIn(f"generate new code: {self._generated_type_path}\n", result.output)
        self.assertIn(f"generate new code: {self._generated_provider_test_path}\n", result.output)
        self.assertIn(f"generate new code: {self._generated_type_test_path}\n", result.output)
        self.assertIn(f"generate new code: {self._generated_acceptance_test_path}\n", result.output)

        self.assertTrue(os.path.exists(self._generated_provider_path))
        self.assertTrue(os.path.exists(self._generated_type_path))
        self.assertTrue(os.path.exists(self._generated_type_test_path))
        self.assertTrue(os.path.exists(self._generated_provider_test_path))
        self.assertTrue(os.path.exists(self._generated_acceptance_test_path))

        provider_file_content = self._read_file(self._generated_provider_path)
        type_file_content = self._read_file(self._generated_type_path)
        type_test_file_content = self._read_file(self._generated_type_test_path)
        provider_test_file_content = self._read_file(self._generated_provider_test_path)
        acceptance_test_file_content = self._read_file(self._generated_acceptance_test_path)

        self._test_provider_file_content(provider_file_content)
        self._test_type_file_content(type_file_content)
        self._test_type_test_file_content(type_test_file_content)
        self._test_provider_test_file_content(provider_test_file_content)
        self._test_acceptance_test_file_content(acceptance_test_file_content)

    def _test_provider_file_content(self, file_content):
        self.assertIn(
            "def initialize\n"
            "        super\n"
            "        @group = \'haproxy\'\n"
            "        @command = \'frontend\'\n"
            "        @resource_type = \'list\'\n"
            "        @find_uuid_by_column = :name\n"
            "        @create_key = :name\n"
            "    end\n\n""",
            file_content
        )

        self.assertIn(
            "name: json_object['name']",
            file_content
        )

        self.assertIn(
            "enabled: bool_from_value(json_object['enabled']),",
            file_content
        )

        self.assertIn(
            "defaultbackend: array_from_value(json_object['defaultbackend']),",
            file_content
        )

        self.assertIn(
            "args.push('--name', puppet_resource[:name]) if mode == 'update'",
            file_content
        )

        self.assertIn(
            "args.push('--enabled') if bool_from_value(puppet_resource[:enabled]) == true",
            file_content
        )
        self.assertIn(
            "args.push('--no-enabled') if bool_from_value(puppet_resource[:enabled]) == false",
            file_content
        )

        self.assertIn(
            "puppet_resource[:ssl_bindoptions].each do |opt|\n"
            "          args.push(\'--ssl_bindoptions\', opt)\n"
            "        end\n",
            file_content
        )

        self.assertIn(
            "args.push('--linkedcpuaffinityrules', puppet_resource[:linkedcpuaffinityrules].join(','))",
            file_content
        )

    def _test_type_file_content(self, file_content):
        pass

    def _test_type_test_file_content(self, type_test_file_content):
        pass

    def _test_provider_test_file_content(self, provider_test_file_content):
        pass

    def _test_acceptance_test_file_content(self, acceptance_test_file_content):
        pass

