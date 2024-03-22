from opnsense_cli.factories import ClassFromKeymapFactory
from opnsense_cli.formatters.cli_output.output_formats import (
    ColsOutputFormat,
    JsonFilterOutputFormat,
    JsonOutputFormat,
    PlainOutputFormat,
    TableOutputFormat,
    YamlOutputFormat,
)


class CliOutputFormatFactory(ClassFromKeymapFactory):
    _keymap = {
        "cols": ColsOutputFormat,
        "table": TableOutputFormat,
        "json": JsonOutputFormat,
        "json_filter": JsonFilterOutputFormat,
        "plain": PlainOutputFormat,
        "yaml": YamlOutputFormat,
    }
