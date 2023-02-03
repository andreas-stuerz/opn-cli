import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, available_formats
from opnsense_cli.commands.core.ipsec import tunnel
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.core.ipsec import Tunnel
from opnsense_cli.facades.commands.core.ipsec.tunnel import IpsecTunnelFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_ipsec_tunnel_svc = click.make_pass_decorator(IpsecTunnelFacade)


@tunnel.group()
@pass_api_client
@click.pass_context
def phase2(ctx, api_client: ApiClient, **kwargs):
    """
    Manage ipsec phase 2 tunnels
    """
    tunnel_api = Tunnel(api_client)
    ctx.obj = IpsecTunnelFacade(tunnel_api)


@phase2.command()
@click.option(
    '--output', '-o',
    help='Specifies the Output format.',
    default="table",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    default=(
            "id,uniqid,ikeid,reqid,enabled,protocol,mode,local_subnet,remote_subnet,proposal,description"
    ),
    show_default=True,
)
@pass_ipsec_tunnel_svc
def list(ipsec_tunnel_svc: IpsecTunnelFacade, **kwargs):
    """
    Show all ipsec phase2 tunnels
    """

    result = ipsec_tunnel_svc.list_phase2_tunnels()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@phase2.command()
@click.argument('uniqid')
@click.option(
    '--output', '-o',
    help='Specifies the Output format.',
    default="table",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    default=(
            "id,uniqid,ikeid,reqid,enabled,protocol,mode,local_subnet,remote_subnet,proposal,description"
    ),
    show_default=True,
)
@pass_ipsec_tunnel_svc
def show(ipsec_tunnel_svc: IpsecTunnelFacade, **kwargs):
    """
    Show details for phase 2 tunnel
    """
    result = ipsec_tunnel_svc.show_phase2_tunnels(kwargs['uniqid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
