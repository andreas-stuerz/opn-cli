import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats, int_as_string, tuple_to_csv
from opnsense_cli.types.click_param_type.int_or_empty import INT_OR_EMPTY
from opnsense_cli.commands.core.unbound import unbound
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.core.unbound import Settings, Service
from opnsense_cli.facades.commands.core.unbound.host import UnboundHostFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_unbound_host_svc = click.make_pass_decorator(UnboundHostFacade)


@unbound.group()
@pass_api_client
@click.pass_context
def host(ctx, api_client: ApiClient, **kwargs):
    """
    Manage host overrides
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = UnboundHostFacade(settings_api, service_api)


@host.command()
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
        "uuid,enabled,hostname,domain,rr,mxprio,mx,server,description"
    ),
    show_default=True,
)
@pass_unbound_host_svc
def list(unbound_host_svc: UnboundHostFacade, **kwargs):
    """
    Show all hosts overrides
    """
    result = unbound_host_svc.list_hosts()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@host.command()
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
        "enabled,hostname,domain,rr,mxprio,mx,server,description"
    ),
    show_default=True,
)
@pass_unbound_host_svc
def show(unbound_host_svc: UnboundHostFacade, **kwargs):
    """
    Show details for host override
    """
    result = unbound_host_svc.show_host(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@host.command()
@click.option(
    '--enabled/--no-enabled',
    help=('Enable the override for this host.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--hostname',
    help=('Name of the host, without the domain part. Use "*" to create a wildcard entry.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--domain',
    help=('Domain of the host, e.g. example.com'),
    show_default=True,
    default=None,
    required=True,
)
@click.option(
    '--rr',
    help=('Type of resource record, e.g. A or AAAA for IPv4 or IPv6 addresses'),
    type=click.Choice(['A', 'AAAA', 'MX']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='A',
    required=True,
)
@click.option(
    '--mxprio',
    help=('Priority of MX record, e.g. 10'),
    show_default=True,
    type=INT_OR_EMPTY,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--mx',
    help=('Host name of MX host, e.g. mail.example.com'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--server',
    help=('IP address of the host, e.g. 192.168.100.100 or fd00:abcd::1ne'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--description',
    help=('You may enter a description here for your reference (not parsed)'),
    show_default=True,
    default=None,
    required=False,
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
@pass_unbound_host_svc
def create(unbound_host_svc: UnboundHostFacade, **kwargs):
    """
    Create a new host override
    """
    json_payload = {
        'host': {
            "enabled": kwargs['enabled'],
            "hostname": kwargs['hostname'],
            "domain": kwargs['domain'],
            "rr": kwargs['rr'],
            "mxprio": kwargs['mxprio'],
            "mx": kwargs['mx'],
            "server": kwargs['server'],
            "description": kwargs['description'],
        }
    }

    result = unbound_host_svc.create_host(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@host.command()
@click.argument('uuid')
@click.option(
    '--enabled/--no-enabled',
    help=('Enable the override for this host.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--hostname',
    help=('Name of the host, without the domain part. Use "*" to create a wildcard entry.'),
    show_default=True,
    default=None
)
@click.option(
    '--domain',
    help=('Domain of the host, e.g. example.com'),
    show_default=True,
    default=None
)
@click.option(
    '--rr',
    help=('Type of resource record, e.g. A or AAAA for IPv4 or IPv6 addresses'),
    type=click.Choice(['A', 'AAAA', 'MX']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--mxprio',
    help=('Priority of MX record, e.g. 10'),
    show_default=True,
    type=INT_OR_EMPTY,
    callback=int_as_string,
    default=None
)
@click.option(
    '--mx',
    help=('Host name of MX host, e.g. mail.example.com'),
    show_default=True,
    default=None
)
@click.option(
    '--server',
    help=('IP address of the host, e.g. 192.168.100.100 or fd00:abcd::1ne'),
    show_default=True,
    default=None
)
@click.option(
    '--description',
    help=('You may enter a description here for your reference (not parsed)'),
    show_default=True,
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
@pass_unbound_host_svc
def update(unbound_host_svc: UnboundHostFacade, **kwargs):
    """
    Update a host override
    """
    json_payload = {
        'host': {}
    }
    options = ['enabled', 'hostname', 'domain', 'rr', 'mxprio', 'mx', 'server', 'description']
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['host'][option] = kwargs[option.lower()]

    result = unbound_host_svc.update_host(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@host.command()
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
@pass_unbound_host_svc
def delete(unbound_host_svc: UnboundHostFacade, **kwargs):
    """
    Delete a host override
    """
    result = unbound_host_svc.delete_host(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
