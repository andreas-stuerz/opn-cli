import os
import json
from pyfakefs.fake_filesystem_unittest import TestCase
from unittest.mock import Mock

import opnsense_cli


class BaseTestCase(TestCase):
    BASE_DIR = os.path.dirname(opnsense_cli.__file__)

    def _read_json_fixture(self, relative_path):
        path = self._get_fixture_path(relative_path)
        file_content = self._read_file(path)
        return json.loads(file_content)

    def _read_fixture_file(self, relative_path):
        path = self._get_fixture_path(relative_path)
        file_content = self._read_file(path)
        return file_content

    def _read_template_file(self, relative_path):
        path = os.path.join(self.BASE_DIR, relative_path)
        file_content = self._read_file(path)
        return file_content

    def _get_fixture_path(self, relative_path, fixture_dir="../fixtures/tests/commands"):
        path = os.path.join(os.path.dirname(__file__), fixture_dir, relative_path)
        return os.path.abspath(path)

    def _get_output_path(self, relative_path, output_dir="../../output"):
        path = os.path.join(os.path.dirname(__file__), output_dir, relative_path)
        return os.path.abspath(path)

    def _read_file(self, path):
        with open(path) as file:
            content = file.read()
        return content

    def _setup_fakefs(self):
        self.setUpPyfakefs()
        self.fs.add_real_directory(self.BASE_DIR)

    def _show_fakefs_contents(self):
        for file in os.walk("/"):
            print(file)

    def _mock_response(self, status=200, content="CONTENT", json_data=None, raise_for_status=None):
        """Mock Response obj for request library"""
        mock_resp = Mock()

        mock_resp.raise_for_status = Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status

        mock_resp.status_code = status
        mock_resp.content = content

        if json_data:
            mock_resp.json = Mock(return_value=json_data)

        return mock_resp
