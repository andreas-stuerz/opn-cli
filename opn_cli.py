#!/usr/bin/env python3
import click
import yaml

from opnsense_api.client import ApiClient

# import commands
from commands.plugin import plugin
from commands.firewall import firewall

DEFAULT_CFG = '~/.opn-cli-conf.yaml'

def configure(ctx, param, filename):
    def dict_from_yaml(path):
        with open(path, 'r') as yaml_file:
            data = yaml.load(yaml_file, Loader=yaml.SafeLoader)
        return data
    try:
        options = dict_from_yaml(filename)
    except KeyError:
        options = {}
    ctx.default_map = options

@click.group()
@click.option(
    '--config', '-c',
    help='path to the config file',
    type=click.Path(dir_okay=False),
    envvar="OPN_CONFIG",
    default=DEFAULT_CFG,
    show_default=True,
    callback = configure,
    is_eager=True,
    expose_value=False,
)
@click.option(
    '--api-key', '-k',
    help='Your API key for the OPNsense API',
    envvar="OPN_API_KEY",
)
@click.option(
    '--api-secret', '-s',
    help='Your API secret for the OPNsense API',
    envvar="OPN_API_SECRET",
)
@click.option(
    '--url', '-u',
    help='The Base URL for the OPNsense API',
    envvar="OPN_API_URL",
    default="https://127.0.0.1/api"
)
@click.option(
    '--timeout', '-t',
    help='Set timeout for API Calls in seconds.',
    envvar="OPN_API_TIMEOUT",
    default=60,
)
@click.option(
    '--ssl-verify/--no-ssl-verify',
    help='Enable or disable SSL verification for API communication.',
    envvar="OPN_SSL_VERIFY",
    is_flag=True,
    default=True,
)
@click.pass_context
def cli(ctx, **kwargs):
    """
    OPNsense CLI - interact with OPNsense via the API

    You need a valid API key and secret to interact with the API.
    Goto System->Access->Users and use a existing or generate an Api Key.

    You can set the required options as environment variables:
    export OPN_API_KEY="<your-api-key>"
    export OPN_API_SECRET="<your-api-secret>"
    export OPN_API_URL="https://127.0.0.1/api"
    export OPN_SSL_VERIFY=1
    export OPN_API_TIMEOUT=60

    Or use a config file passed with -c option.

    The configuration cascade from highest precedence to lowest:

    1. argument & options

    2. environment variables

    3. config file

    """
    ctx.obj = ApiClient(kwargs['api_key'], kwargs['api_secret'], kwargs['url'], kwargs['ssl_verify'], kwargs['timeout'])
    pass

# register commands
cli.add_command(plugin)
cli.add_command(firewall)


if __name__ == "__main__":
    cli()
