import click

from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import formatter_from_formatter_name, available_formats
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.openvpn import Openvpn

pass_api_client = click.make_pass_decorator(ApiClient)
pass_openvpn_svc = click.make_pass_decorator(Openvpn)


@click.group()
@pass_api_client
@click.pass_context
def openvpn(ctx, api_client: ApiClient, **kwargs):
    """
    Export OpenVPN configuration.
    """
    ctx.obj = Openvpn(api_client)


@openvpn.command()
@click.argument('vpnid')
@click.option(
    '--output', '-o',
    help=' Output format.',
    default="table",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    default="<ID>,description,users",
    show_default=True,
)
@pass_openvpn_svc
def accounts(openvpn_svc: Openvpn, **kwargs):
    """
    Show all accounts for a OpenVPN server.

    VPNID is the ID of the OpenVPN server (use "providers" to get a list).
    """
    result = openvpn_svc.accounts(kwargs['vpnid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@openvpn.command()
@click.argument('vpnid')
@click.argument('certref')
@click.option(
    '--auth_nocache',
    default="0",
    type=int,
    show_default=True,
)
@click.option(
    '--cryptoapi',
    default="0",
    type=int,
    show_default=True,
)
@click.option(
    '--hostname',
    type=str,
    required=False,
)
@click.option(
    '--local_port',
    default="1194",
    type=int,
    show_default=True,
)
@click.option(
    '--p12_password',
    type=str,
    required=False,
)
@click.option(
    '--p12_password_confirm',
    type=str,
    required=False,
)
@click.option(
    '--plain_config',
    type=str,
    required=False,
)
@click.option(
    '--random_local_port',
    default="1",
    type=int,
    required=False,
    show_default=True,
)
@click.option(
    '--servers',
    type=int,
    required=False,
    show_default=True,
)
@click.option(
    '--template',
    default="PlainOpenVPN",
    type=str,
    show_default=True,
)
@click.option(
    '--validate_server_cn',
    default="1",
    type=int,
    show_default=True,
)
@click.option(
    '--output', '-o',
    help=' Output format.',
    default="plain",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    # NOTE: "content" is base64 encoded, otherwise the binary content
    # would scramble the console. (Whether or not binary content is actually
    # returned by the API depends on the value of --template.)
    default="filename,content",
    show_default=True,
)
@pass_openvpn_svc
def download(openvpn_svc: Openvpn, **kwargs):
    """
    Download client config for chosen OpenVPN server and account.

    VPNID is the ID of the OpenVPN server (use "providers" to get a list).
    CERTREF is the ID of the OpenVPN account (use "accounts" to get a list).
    """
    json = {
        'openvpn_export': {
        }
    }
    options = [
        'auth_nocache', 'cryptoapi', 'hostname', 'local_port', 'p12_password', 'p12_password_confirm', 'plain_config',
        'random_local_port', 'servers', 'template', 'validate_server_cn'
    ]
    for option in options:
        if kwargs[option] is not None:
            json['openvpn_export'][option] = kwargs[option]

    result = openvpn_svc.download(kwargs['vpnid'], kwargs['certref'], json=json)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@openvpn.command()
@click.option(
    '--output', '-o',
    help=' Output format.',
    default="table",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    default="<ID>,name,mode,vpnid,hostname,template,local_port",
    show_default=True,
)
@pass_openvpn_svc
def providers(openvpn_svc: Openvpn, **kwargs):
    """
    Show all available OpenVPN servers.
    """
    result = openvpn_svc.providers()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@openvpn.command()
@click.option(
    '--output', '-o',
    help=' Output format.',
    default="table",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    default="<ID>,name,supportedOptions",
    show_default=True,
)
@pass_openvpn_svc
def templates(openvpn_svc: Openvpn, **kwargs):
    """
    Show all available export templates.
    """
    result = openvpn_svc.templates()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
