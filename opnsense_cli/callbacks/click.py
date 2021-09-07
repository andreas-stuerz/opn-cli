import yaml
import os
from opnsense_cli.factories.cli_output_format import CliOutputFormatFactory
from opnsense_cli.formats.base import Format

"""
Click callback methods
See: https://click.palletsprojects.com/en/8.0.x/advanced/#parameter-modifications
"""


def defaults_from_configfile(ctx, param, filename):
    def dict_from_yaml(path):
        with open(path, 'r') as yaml_file:
            data = yaml.load(yaml_file, Loader=yaml.SafeLoader)
        return data
    options = dict_from_yaml(os.path.expanduser(filename))
    ctx.default_map = options


def expand_path(ctx, param, filename):
    return os.path.expanduser(filename)


def available_formats():
    return CliOutputFormatFactory._keymap.keys()


def formatter_from_formatter_name(ctx, param, format_name) -> Format:
    factory = CliOutputFormatFactory(format_name)
    return factory.get_class()


def bool_as_string(ctx, param, value):
    if type(value) == bool:
        return str(int(value))
    return value


def tuple_to_csv(ctx, param, value):
    if type(value) == tuple:
        return ",".join(value)
    return value


def comma_to_newline(ctx, param, value):
    if type(value) == str and "," in value:
        return value.replace(",", "\n")
    return value


def int_as_string(ctx, param, value):
    if type(value) == int:
        return str(value)
    return value
