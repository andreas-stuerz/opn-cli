from opnsense_cli.factories.base import ClassFromKeymapFactory
from opnsense_cli.formats.json_output import JsonOutputFormat
from opnsense_cli.formats.table_output import TableOutputFormat


class CliOutputFormatFactory(ClassFromKeymapFactory):
    _keymap = {
        'json': JsonOutputFormat,
        'table': TableOutputFormat
    }
