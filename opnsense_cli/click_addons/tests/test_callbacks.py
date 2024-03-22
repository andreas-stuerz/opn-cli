import unittest
from unittest.mock import patch
from opnsense_cli.click_addons.callbacks import get_default_config_dir, bool_as_string, comma_to_newline
from opnsense_cli import __cli_name__
import os


class TestClickCallbacks(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_get_default_config_dir(self):
        result = get_default_config_dir()
        self.assertEqual(result, f"~/.{__cli_name__}")

    @patch.dict(os.environ, {"XDG_CONFIG_HOME": "whatever"}, clear=True)
    def test_get_default_config_dir_xgd_home(self):
        result = get_default_config_dir()
        self.assertEqual(result, f"~/.config/{__cli_name__}")

    def test_bool_as_string_with_bool(self):
        result = bool_as_string(None, None, True)
        self.assertEqual(result, "1")

    def test_bool_as_string_without_bool(self):
        result = bool_as_string(None, None, 5)
        self.assertEqual(result, 5)

    def test_comma_to_newline_with_csv_string(self):
        result = comma_to_newline(None, None, "item1,item2,item3")
        self.assertEqual(result, "item1\nitem2\nitem3")

    def test_comma_to_newline_without_csv_string(self):
        result = comma_to_newline(None, None, "item1")
        self.assertEqual(result, "item1")
