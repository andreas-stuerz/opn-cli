import yaml
import os
from opnsense_cli.format_maps.cli_output_format import CliOutputFormatMap
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


def formatter_from_formatter_name(ctx, param, format_name) -> Format:
    format_map = CliOutputFormatMap(format_name)
    return format_map.get_formatter()
