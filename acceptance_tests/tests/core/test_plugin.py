from acceptance_tests.base import CliCommandTestCase


class TestPluginCommands(CliCommandTestCase):
    def setUp(self):
        pass

    def test_plugin_lifecycle(self):
        result = self.run_command("opn-cli plugin installed -o plain -c name,locked")
        self.assertIn(
            "os-firewall N/A\n"
            "os-haproxy N/A\n"
            "os-virtualbox N/A\n",
            result.stdout
        )

        result = self.run_command("opn-cli plugin install os-helloworld")
        assert result.exitcode == 0

        result = self.run_command("opn-cli plugin lock os-helloworld")
        assert result.exitcode == 0

        result = self.run_command("opn-cli plugin installed -o plain -c name,locked")
        self.assertIn(
            "os-firewall N/A\n"
            "os-haproxy N/A\n"
            "os-helloworld 1\n"
            "os-virtualbox N/A\n",
            result.stdout
        )

        result = self.run_command("opn-cli plugin unlock os-helloworld")
        assert result.exitcode == 0

        result = self.run_command("opn-cli plugin uninstall os-helloworld")
        assert result.exitcode == 0
