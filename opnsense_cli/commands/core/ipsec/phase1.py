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
def phase1(ctx, api_client: ApiClient, **kwargs):
    """
    Manage ipsec phase 1 tunnels
    """
    tunnel_api = Tunnel(api_client)
    ctx.obj = IpsecTunnelFacade(tunnel_api)


@phase1.command()
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
            "id,seqid,enabled,protocol,iketype,interface,remote_gateway,mobile,mode,proposal,authentication,description,type"
    ),
    show_default=True,
)
@pass_ipsec_tunnel_svc
def list(ipsec_tunnel_svc: IpsecTunnelFacade, **kwargs):
    """
    Show all ipsec phase1 tunnels
    """
    result = ipsec_tunnel_svc.list_phase1_tunnels()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@phase1.command()
@click.argument('ikeid')
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
        "id,seqid,enabled,protocol,iketype,interface,remote_gateway,mobile,mode,proposal,authentication,description,type"
    ),
    show_default=True,
)
@pass_ipsec_tunnel_svc
def show(ipsec_tunnel_svc: IpsecTunnelFacade, **kwargs):
    """
    Show details for phase 1 tunnel
    """
    result = ipsec_tunnel_svc.show_phase1_tunnels(kwargs['ikeid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
