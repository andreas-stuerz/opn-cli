import shlex
import subprocess
from dataclasses import dataclass
from unittest import TestCase


class CommandError(Exception):
    def __init__(self, code, msg):
        message = "Exit code: {} - Error: {}".format(code, msg)
        super().__init__(message)


@dataclass
class CommandResult:
    stdout: str
    stderr: str
    exitcode: int


class CliCommandTestCase(TestCase):
    @property
    def _api_client_args_fixtures(self):
        return [
            'api_key',
            'api_secret',
            'https://127.0.0.1:10443/api',
            True,
            '~/.opn-cli/ca.pem',
            60
        ]

    def run_command(self, command) -> str:
        """
        :param command: The cli command
        :return: str
        """
        return self.cmd_execute(command)

    def cmd_execute(self, command, encoding='UTF-8', raise_exception=False):
        args = shlex.split(command)
        p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p.communicate()
        if error and raise_exception:
            raise CommandError(p.returncode, error.decode(encoding))

        result = CommandResult(
            output.decode(encoding),
            error.decode(encoding),
            p.returncode
        )

        return result
