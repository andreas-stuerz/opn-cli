from opnsense_cli.format_maps.base import FormatterMap
from opnsense_cli.formats.json import JsonFormat
from opnsense_cli.formats.table import TableFormat


class CliOutputFormatMap(FormatterMap):
    _format_map = {
        'json': JsonFormat,
        'table': TableFormat
    }
