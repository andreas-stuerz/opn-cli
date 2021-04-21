#!/usr/bin/env python3
import click
import yaml
import os

from opnsense_cli.api.client import ApiClient
from opnsense_cli.command.version import version
from opnsense_cli.command.plugin import plugin
from opnsense_cli.command.firewall import firewall


CFG_DIR = "~/.opn-cli"
DEFAULT_CFG = f"{CFG_DIR}/conf.yaml"
DEFAULT_SSL_VERIFY_CA = f"{CFG_DIR}/ca.pem"
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def defaults_from_configfile(ctx, param, filename):
    def dict_from_yaml(path):
        with open(path, 'r') as yaml_file:
            data = yaml.load(yaml_file, Loader=yaml.SafeLoader)
        return data

    try:
        options = dict_from_yaml(os.path.expanduser(filename))
    except KeyError:
        options = {}
    ctx.default_map = options


def expand_path(ctx, param, filename):
    return os.path.expanduser(filename)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    '--config', '-c',
    help='path to the config file',
    type=click.Path(dir_okay=False),
    envvar="OPN_CONFIG",
    default=DEFAULT_CFG,
    show_default=True,
    callback=defaults_from_configfile,
    is_eager=True,
    expose_value=False,
    show_envvar=True,
)
@click.option(
    '--ca',
    help='path to the ca bundle file for ssl verification',
    type=click.Path(dir_okay=False),
    envvar="OPN_SSL_VERIFY_CA",
    default=DEFAULT_SSL_VERIFY_CA,
    is_eager=True,
    show_default=True,
    callback=expand_path,
    show_envvar=True,
)
@click.option(
    '--api-key', '-k',
    help='Your API key for the OPNsense API',
    envvar="OPN_API_KEY",
    show_envvar=True,
)
@click.option(
    '--api-secret', '-s',
    help='Your API secret for the OPNsense API',
    envvar="OPN_API_SECRET",
    show_envvar=True,
)
@click.option(
    '--url', '-u',
    help='The Base URL for the OPNsense API',
    envvar="OPN_API_URL",
    default="https://127.0.0.1/api",
    show_envvar=True,
)
@click.option(
    '--timeout', '-t',
    help='Set timeout for API Calls in seconds.',
    envvar="OPN_API_TIMEOUT",
    default=60,
    show_envvar=True,
    show_default=True,
)
@click.option(
    '--ssl-verify/--no-ssl-verify',
    help='Enable or disable SSL verification for API communication.',
    envvar="OPN_SSL_VERIFY",
    is_flag=True,
    default=True,
    show_envvar=True,
    show_default=True,
)
@click.pass_context
def cli(ctx, **kwargs):
    """
    OPNsense CLI - interact with OPNsense via the API

    You need a valid API key and secret to interact with the API.
    Open your browser and go to System->Access->Users and generate or use an existing Api Key.

    If you use ssl verification (--ssl-verify), make sure to specify a valid ca with --ca <path_to_bundle>.

    You can set the required options as environment variables. See --help "[env var: [...]"

    Or use a config file passed with -c option.

    The configuration cascade from highest precedence to lowest:

    1. argument & options

    2. environment variables

    3. config file

    """
    ctx.obj = ApiClient(
        kwargs['api_key'],
        kwargs['api_secret'],
        kwargs['url'],
        kwargs['ssl_verify'],
        kwargs['ca'],
        kwargs['timeout'],
    )


# register commands
cli.add_command(version)
cli.add_command(plugin)
cli.add_command(firewall)

if __name__ == "__main__":
    cli()
