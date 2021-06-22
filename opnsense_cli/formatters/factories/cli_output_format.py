from opnsense_cli.formatters.factories.base import FormatFactory
from opnsense_cli.formatters.formats.json_output import JsonOutputFormat
from opnsense_cli.formatters.formats.table_output import TableOutputFormat


class CliOutputFormatFactory(FormatFactory):
    _format_map = {
        'json': JsonOutputFormat,
        'table': TableOutputFormat
    }
