from opnsense_cli.factories.base import ClassFromKeymapFactory
from opnsense_cli.formats.json_filter_output import JsonFilterOutputFormat
from opnsense_cli.formats.json_output import JsonOutputFormat
from opnsense_cli.formats.table_output import TableOutputFormat
from opnsense_cli.formats.yaml_output import YamlOutputFormat


class CliOutputFormatFactory(ClassFromKeymapFactory):
    _keymap = {
        'json': JsonOutputFormat,
        'json_filter': JsonFilterOutputFormat,
        'table': TableOutputFormat,
        'yaml': YamlOutputFormat,
    }
