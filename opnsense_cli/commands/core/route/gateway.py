import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, available_formats
from opnsense_cli.commands.core.route import route
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.core.routes import Gateway
from opnsense_cli.facades.commands.core.route.gateway import RoutesGatewayFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_routes_gateway_svc = click.make_pass_decorator(RoutesGatewayFacade)


@route.group()
@pass_api_client
@click.pass_context
def gateway(ctx, api_client: ApiClient, **kwargs):
    """
    Manage gateway routes
    """
    gateway_api = Gateway(api_client)
    ctx.obj = RoutesGatewayFacade(gateway_api)


@gateway.command()
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
        "name,address,status,status_translated,loss,stddev,delay"
    ),
    show_default=True,
)
@pass_routes_gateway_svc
def status(routes_gateway_svc: RoutesGatewayFacade, **kwargs):
    """
    Show gateway states
    """
    result = routes_gateway_svc.show_status()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
