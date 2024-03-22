#!/usr/bin/env python3
import click


from opnsense_cli.click_addons.callbacks import defaults_from_configfile, expand_path, get_default_config_dir
from opnsense_cli.api.client import ApiClient
from opnsense_cli.click_addons.command_autoloader import ClickCommandAutoloader
from opnsense_cli.click_addons.command_tree import _build_command_tree, _print_tree

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--config",
    "-c",
    help="path to the config file",
    type=click.Path(dir_okay=False),
    envvar="OPN_CONFIG",
    default=f"{get_default_config_dir()}/conf.yaml",
    show_default=True,
    callback=defaults_from_configfile,
    is_eager=True,
    expose_value=False,
    show_envvar=True,
)
@click.option(
    "--ca",
    help="path to the ca bundle file for ssl verification",
    type=click.Path(dir_okay=False),
    envvar="OPN_SSL_VERIFY_CA",
    default=f"{get_default_config_dir()}/ca.pem",
    is_eager=True,
    show_default=True,
    callback=expand_path,
    show_envvar=True,
)
@click.option(
    "--api-key",
    "-k",
    help="Your API key for the OPNsense API",
    envvar="OPN_API_KEY",
    show_envvar=True,
)
@click.option(
    "--api-secret",
    "-s",
    help="Your API secret for the OPNsense API",
    envvar="OPN_API_SECRET",
    show_envvar=True,
)
@click.option(
    "--url",
    "-u",
    help="The Base URL for the OPNsense API",
    envvar="OPN_API_URL",
    default="https://127.0.0.1/api",
    show_envvar=True,
)
@click.option(
    "--timeout",
    "-t",
    help="Set timeout for API Calls in seconds.",
    envvar="OPN_API_TIMEOUT",
    default=60,
    show_envvar=True,
    show_default=True,
)
@click.option(
    "--ssl-verify/--no-ssl-verify",
    help="Enable or disable SSL verification for API communication.",
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
    ca or cert with --ca <path_to_bundle>.

    To download the default self-signed cert, open the OPNsense Web Gui and go to
    System->Trust->Certificates. Search for the Name: "Web GUI SSL certificate" and
    press the "export user cert" button.

    If you use a ca signed certificate, go to System->Trust->Authorities and
    press the "export CA cert" button to download the ca.

    Save the ca and pass the path to the --ca option.

    Configuration:

    The base directory for the config is ~/.opn-cli.

    If the environment variable XDG_CONFIG_HOME is set, ~/.config/opn-cli will be used instead.

    You can set the required options as environment variables. See --help
    "[env var: [...]"

    Or use a config file passed with -c option.

    The configuration cascade from the highest precedence to lowest:

    1. argument & options

    2. environment variables

    3. config file

    Happy automating!
    """
    ctx.obj = ApiClient(
        kwargs["api_key"],
        kwargs["api_secret"],
        kwargs["url"],
        kwargs["ssl_verify"],
        kwargs["ca"],
        kwargs["timeout"],
    )


autoloader = ClickCommandAutoloader(cli)
autoloader.autoload("opnsense_cli.commands.core")
autoloader.autoload("opnsense_cli.commands.plugin")
autoloader.autoload("opnsense_cli.commands.new")
autoloader.autoload("opnsense_cli.commands.completion")
autoloader.autoload("opnsense_cli.commands.version")
autoloader.autoload("opnsense_cli.commands.tree")

if __name__ == "__main__":
    cli()
