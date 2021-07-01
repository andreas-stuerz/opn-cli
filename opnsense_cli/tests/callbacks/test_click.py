import unittest
import opnsense_cli.callbacks.click as callbacks


class TestClickCallbacks(unittest.TestCase):
    def test_bool_as_string_with_bool(self):
        result = callbacks.bool_as_string(None, None, True)
        self.assertEqual(result, '1')

    def test_bool_as_string_without_bool(self):
        result = callbacks.bool_as_string(None, None, 5)
        self.assertEqual(result, 5)

    def test_comma_to_newline_with_csv_string(self):
        result = callbacks.comma_to_newline(None, None, 'item1,item2,item3')
        self.assertEqual(result, 'item1\nitem2\nitem3')

    def test_comma_to_newline_without_csv_string(self):
        result = callbacks.comma_to_newline(None, None, 'item1')
        self.assertEqual(result, 'item1')
