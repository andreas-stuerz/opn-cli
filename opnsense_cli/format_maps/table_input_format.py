from opnsense_cli.format_maps.base import FormatterMap


class TableFormatInputMap(FormatterMap):
    def _format_map(self):
        return {
            'json': "",
            'table': ""
        }
