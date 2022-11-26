import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats
from opnsense_cli.commands.core.route import route
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.core.routes import Routes, Gateway
from opnsense_cli.facades.commands.core.route.static import RoutesStaticFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_routes_static_svc = click.make_pass_decorator(RoutesStaticFacade)


@route.group()
@pass_api_client
@click.pass_context
def static(ctx, api_client: ApiClient, **kwargs):
    """
    Manage static routes
    """
    routes_api = Routes(api_client)
    gateway_api = Gateway(api_client)
    ctx.obj = RoutesStaticFacade(routes_api, gateway_api)


@static.command()
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
        "uuid,network,gateway,descr,disabled"
    ),
    show_default=True,
)
@pass_routes_static_svc
def list(routes_static_svc: RoutesStaticFacade, **kwargs):
    """
    Show all static routes
    """
    result = routes_static_svc.list_statics()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@static.command()
@click.argument('uuid')
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
        "network,gateway,descr,disabled"
    ),
    show_default=True,
)
@pass_routes_static_svc
def show(routes_static_svc: RoutesStaticFacade, **kwargs):
    """
    Show details for a static route
    """
    result = routes_static_svc.show_static(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@static.command()
@click.option(
    '--network',
    help=('Destination network for this static route'),
    show_default=True,
    default=None,
    required=True,
)
@click.option(
    '--gateway',
    help=(
        'Choose which gateway this route applies to eg. Null4 for 127.0.01, Null6 for ::1 or see opn-cli route gateway status.'
    ),
    show_default=True,
    default=None,
    required=True,
)
@click.option(
    '--descr',
    help=('You may enter a description here for your reference (not parsed).'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--disabled/--no-disabled',
    help=('Set this option to disable this static route without removing it from the list.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--output', '-o',
    help='Specifies the Output format.',
    default="plain",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    default="result,validations",
    show_default=True,
)
@pass_routes_static_svc
def create(routes_static_svc: RoutesStaticFacade, **kwargs):
    """
    Create a new static route
    """
    json_payload = {
        'route': {
            "network": kwargs['network'],
            "gateway": kwargs['gateway'],
            "descr": kwargs['descr'],
            "disabled": kwargs['disabled'],
        }
    }

    result = routes_static_svc.create_static(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@static.command()
@click.argument('uuid')
@click.option(
    '--network',
    help=('Destination network for this static route'),
    show_default=True,
    default=None
)
@click.option(
    '--gateway',
    help=(
        'Choose which gateway this route applies to eg. Null4 for 127.0.01, Null6 for ::1 or see opn-cli route gateway status.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--descr',
    help=('You may enter a description here for your reference (not parsed).'),
    show_default=True,
    default=None
)
@click.option(
    '--disabled/--no-disabled',
    help=('Set this option to disable this static route without removing it from the list.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--output', '-o',
    help='Specifies the Output format.',
    default="plain",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    default="result,validations",
    show_default=True,
)
@pass_routes_static_svc
def update(routes_static_svc: RoutesStaticFacade, **kwargs):
    """
    Update a static route
    """
    json_payload = {
        'route': {}
    }
    options = ['network', 'gateway', 'descr', 'disabled']
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['route'][option] = kwargs[option.lower()]

    result = routes_static_svc.update_static(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@static.command()
@click.argument('uuid')
@click.option(
    '--output', '-o',
    help='Specifies the Output format.',
    default="plain",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    default="result,validations",
    show_default=True,
)
@pass_routes_static_svc
def delete(routes_static_svc: RoutesStaticFacade, **kwargs):
    """
    Delete static route
    """
    result = routes_static_svc.delete_static(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
