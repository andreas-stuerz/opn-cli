#!/usr/bin/env python3
import click

from opnsense_cli import __cli_name__
from opnsense_cli.callbacks.click import defaults_from_configfile, expand_path
from opnsense_cli.api.client import ApiClient
from opnsense_cli.commands.version import version
from opnsense_cli.commands.completion import completion
from opnsense_cli.commands.plugin import plugin
from opnsense_cli.commands.openvpn import openvpn
from opnsense_cli.commands.firewall import firewall
from opnsense_cli.commands.firewall.alias import alias
from opnsense_cli.commands.firewall.rule import rule


CFG_DIR = f"~/.{__cli_name__}"
DEFAULT_CFG = f"{CFG_DIR}/conf.yaml"
DEFAULT_SSL_VERIFY_CA = f"{CFG_DIR}/ca.pem"
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


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
    OPNsense CLI - interact with OPNsense via the CLI

    API key + secret:

    You need a valid API key and secret to interact with the API. Open your
    browser and go to System->Access->Users and generate or use an existing
    Api Key.

    See: https://docs.opnsense.org/development/how-tos/api.html#creating-keys.

    SSL verify / CA:

    If you use ssl verification (--ssl-verify), make sure to specify a valid
    ca with --ca <path_to_bundle>.

    To download the default self-signed cert, open the OPNsense Web Gui and go to
    System->Trust->Certificates. Search for the Name: "Web GUI SSL certificate" and
    press the "export user cert" button.

    If you use a ca signed certificate, go to System->Trust->Authorities and
    press the "export CA cert" button to download the ca.

    Save the cert or the ca as ~/.opn-cli/ca.pem.

    Configuration:

    You can set the required options as environment variables. See --help
    "[env var: [...]"

    Or use a config file passed with -c option.

    The configuration cascade from highest precedence to lowest:

    1. argument & options

    2. environment variables

    3. config file

    Happy automating!
    """
    ctx.obj = ApiClient(
        kwargs['api_key'],
        kwargs['api_secret'],
        kwargs['url'],
        kwargs['ssl_verify'],
        kwargs['ca'],
        kwargs['timeout'],
    )


# register commands groups and commands
cli.add_command(firewall)
firewall.add_command(alias)
firewall.add_command(rule)

cli.add_command(plugin)
cli.add_command(openvpn)
cli.add_command(version)
cli.add_command(completion)

if __name__ == "__main__":
    cli()
