import os
from opnsense_cli.commands.new.puppet import puppet
from opnsense_cli.tests.commands.base import CommandTestCase
from click.testing import CliRunner


class TestNewPuppetCommands(CommandTestCase):
    def setUp(self):
        self._setup_fakefs()

        self._output_dir = self._get_output_path("")
        self._generated_provider_path = (
            f"{self._output_dir}/puppet/provider/opnsense_haproxy_frontend/opnsense_haproxy_frontend.rb"
        )
        self._generated_type_path = f"{self._output_dir}/puppet/type/opnsense_haproxy_frontend.rb"
        self._generated_type_test_path = f"{self._output_dir}/puppet/spec/unit/puppet/type/opnsense_haproxy_frontend_spec.rb"
        self._generated_provider_test_path = (
            f"{self._output_dir}/puppet/spec/unit/puppet/provider/opnsense_haproxy_frontend_spec.rb"
        )
        self._generated_acceptance_test_path = (
            f"{self._output_dir}/puppet/spec/acceptance/types/opnsense_haproxy_frontend_spec.rb"
        )

    def test_puppet_resource(self):
        runner = CliRunner()
        result = runner.invoke(puppet, ["resource-type", "haproxy", "frontend", "name"], catch_exceptions=True)

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
            "        @group = 'haproxy'\n"
            "        @command = 'frontend'\n"
            "        @resource_type = 'list'\n"
            "        @find_uuid_by_column = :name\n"
            "        @create_key = :name\n"
            "    end\n\n"
            "",
            file_content,
        )

        self.assertIn("name: json_object['name']", file_content)

        self.assertIn("enabled: bool_from_value(json_object['enabled']),", file_content)

        self.assertIn("defaultbackend: array_from_value(json_object['defaultbackend']),", file_content)

        self.assertIn("args.push('--name', puppet_resource[:name]) if mode == 'update'", file_content)

        self.assertIn("args.push('--enabled') if bool_from_value(puppet_resource[:enabled]) == true", file_content)
        self.assertIn("args.push('--no-enabled') if bool_from_value(puppet_resource[:enabled]) == false", file_content)

        self.assertIn(
            "puppet_resource[:ssl_bindoptions].each do |opt|\n"
            "          args.push('--ssl_bindoptions', opt)\n"
            "        end\n",
            file_content,
        )

        self.assertIn(
            "args.push('--linkedcpuaffinityrules', puppet_resource[:linkedcpuaffinityrules].join(','))", file_content
        )

    def _test_type_file_content(self, file_content):
        self.assertIn("name => 'TODO',", file_content)

        self.assertIn("defaultbackend => [],", file_content)
        self.assertIn("forwardfor => TODO,", file_content)

        self.assertIn(
            "    title_patterns: [\n"
            "    {\n"
            "      pattern: %r{^(?<name>.*)@(?<device>.*)$},\n"
            "      desc: 'Where the name and the device are provided with a @',\n"
            "    },\n"
            "    {\n"
            "      pattern: %r{^(?<name>.*)$},\n"
            "      desc: 'Where only the name is provided',\n"
            "    },\n"
            "  ],\n",
            file_content,
        )

        self.assertIn(
            "    description: {\n"
            "      type: 'String',\n"
            "      desc: 'Description for this public service.',\n"
            "    },\n",
            file_content,
        )

        self.assertIn(
            "    mode: {\n"
            "      type: \"Enum['http', 'ssl', 'tcp']\",\n"
            "      desc: 'Set the running mode or protocol for this public service.',\n"
            "    },\n",
            file_content,
        )

        self.assertIn(
            "    http2enabled: {\n" "      type: 'Boolean',\n" "      desc: 'Enable support for HTTP/2.',\n" "    },\n",
            file_content,
        )

        self.assertIn(
            "linkederrorfiles: {\n"
            '      type: "Array[String]",\n'
            "      desc: 'Choose error messages to be included in this public service.',\n"
            "      default: []\n"
            "    },\n",
            file_content,
        )

    def _test_type_test_file_content(self, file_content):
        self.assertIn("bind: 'TODO',", file_content)

        self.assertIn("ssl_enabled: true,", file_content)

        self.assertIn("ssl_certificates: [],", file_content)

        self.assertIn(
            "    it 'accepts name' do\n"
            "      haproxy_frontend[:name] = 'a todo string'\n"
            "      expect(haproxy_frontend[:name]).to eq('a todo string')\n"
            "    end\n\n",
            file_content,
        )
        self.assertIn(
            "    it 'accepts mode' do\n"
            "      haproxy_frontend[:mode] = 'a valid TODO choice'\n"
            "      expect(haproxy_frontend[:mode]).to eq('a valid TODO choice')\n"
            "    end\n\n",
            file_content,
        )
        self.assertIn(
            "    it 'accepts ssl_enabled' do\n"
            "      haproxy_frontend[:ssl_enabled] = false\n"
            "      expect(haproxy_frontend[:ssl_enabled]).to eq(:false)\n"
            "    end\n\n",
            file_content,
        )
        self.assertIn(
            "    it 'accepts ssl_bindoptions' do\n"
            "      haproxy_frontend[:ssl_bindoptions] = ['valid_TODO_choice', 'another_valid_TODO_choice']\n"
            "      expect(haproxy_frontend[:ssl_bindoptions]).to eq(['valid_TODO_choice', 'another_valid_TODO_choice'])\n"
            "    end\n\n",
            file_content,
        )
        self.assertIn(
            "    it 'accepts ssl_certificates' do\n"
            "      haproxy_frontend[:ssl_certificates] = ['valid item1', 'valid item2']\n"
            "      expect(haproxy_frontend[:ssl_certificates]).to eq(['valid item1', 'valid item2'])\n"
            "    end\n\n",
            file_content,
        )

    def _test_provider_test_file_content(self, file_content):
        self.assertIn("\"description\": 'TODO',", file_content)
        self.assertIn("\"mode\": 'TODO',", file_content)
        self.assertIn("\"ssl_enabled\": '1',", file_content)
        self.assertIn("\"ssl_bindoptions\": 'TODO',", file_content)
        self.assertIn("\"ssl_certificates\": 'TODO_CSV',", file_content)

        self.assertIn("name: 'example haproxy_frontend TODO_NUMBER',", file_content)

        self.assertIn("mode: 'TODO',", file_content)

        self.assertIn("ssl_enabled: true,", file_content)

        self.assertIn("ssl_bindoptions: 'TODO',", file_content)

        self.assertIn("ssl_certificates: ['TODO_CSV'],", file_content)

    def _test_acceptance_test_file_content(self, file_content):
        self.assertIn("description => 'TODO',", file_content)

        self.assertIn("mode => 'TODO',", file_content)

        self.assertIn("ssl_enabled => false,", file_content)

        self.assertIn("ssl_bindoptions => 'TODO',", file_content)

        self.assertIn("ssl_certificates => []", file_content)

        self.assertIn("expect(r.stdout).to match %r{name: acceptance test item}", file_content)

        self.assertIn("expect(r.stdout).to match %r{description: TODO}", file_content)

        self.assertIn("expect(r.stdout).to match %r{mode: 'TODO'}", file_content)

        self.assertIn("expect(r.stdout).to match %r{ssl_enabled: '0'}", file_content)

        self.assertIn("expect(r.stdout).to match %r{ssl_bindoptions: 'TODO'}", file_content)

        self.assertIn("expect(r.stdout).to match %r{ssl_certificates: '\\[\\]'}", file_content)
