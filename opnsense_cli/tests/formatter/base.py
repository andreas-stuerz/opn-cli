import io
import sys
import unittest

from opnsense_cli.formats.base import Format


class FormatterTestCase(unittest.TestCase):
    def _get_format_output(self, format: Format):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        format.echo()
        sys.stdout = sys.__stdout__
        result = capturedOutput.getvalue()

        return result
