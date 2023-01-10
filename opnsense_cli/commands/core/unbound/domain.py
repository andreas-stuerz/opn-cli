import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats
from opnsense_cli.commands.core.unbound import unbound
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.core.unbound import Settings, Service
from opnsense_cli.facades.commands.core.unbound.domain import UnboundDomainFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_unbound_domain_svc = click.make_pass_decorator(UnboundDomainFacade)


@unbound.group()
@pass_api_client
@click.pass_context
def domain(ctx, api_client: ApiClient, **kwargs):
    """
    Manage unbound domain overrides
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = UnboundDomainFacade(settings_api, service_api)


@domain.command()
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
        "uuid,enabled,domain,server,description"
    ),
    show_default=True,
)
@pass_unbound_domain_svc
def list(unbound_domain_svc: UnboundDomainFacade, **kwargs):
    """
    Show all domain
    """
    result = unbound_domain_svc.list_domains()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@domain.command()
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
        "enabled,domain,server,description"
    ),
    show_default=True,
)
@pass_unbound_domain_svc
def show(unbound_domain_svc: UnboundDomainFacade, **kwargs):
    """
    Show details for domain
    """
    result = unbound_domain_svc.show_domain(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@domain.command()
@click.option(
    '--enabled/--no-enabled',
    help=('Enable this domain override'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--domain',
    help=(
            'Domain to override (NOTE: this does not have to be a valid TLD!),'
            'e.g. \'test\' or \'mycompany.localdomain\' or \'1.168.192.in-addr.arpa\''
    ),
    show_default=True,
    default=None,
    required=True,
)
@click.option(
    '--server',
    help=(
            'IP address of the authoritative DNS server for this domain,'
            'e.g. \'192.168.100.100\'. To use a nondefault port for communication, append an \'@\' with the port number.'
        ),
    show_default=True,
    default=None,
    required=True,
)
@click.option(
    '--description',
    help=('You may enter a description here for your reference (not parsed).'),
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
@pass_unbound_domain_svc
def create(unbound_domain_svc: UnboundDomainFacade, **kwargs):
    """
    Create a new domain
    """
    json_payload = {
        'domain': {
            "enabled": kwargs['enabled'],
            "domain": kwargs['domain'],
            "server": kwargs['server'],
            "description": kwargs['description'],
        }
    }

    result = unbound_domain_svc.create_domain(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@domain.command()
@click.argument('uuid')
@click.option(
    '--enabled/--no-enabled',
    help=('Enable this domain override'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--domain',
    help=(
            'Domain to override (NOTE: this does not have to be a valid TLD!),'
            'e.g. \'test\' or \'mycompany.localdomain\' or \'1.168.192.in-addr.arpa\''
    ),
    show_default=True,
    default=None
)
@click.option(
    '--server',
    help=(
            'IP address of the authoritative DNS server for this domain,'
            'e.g. \'192.168.100.100\'. To use a nondefault port for communication, append an \'@\' with the port number.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--description',
    help=('You may enter a description here for your reference (not parsed).'),
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
@pass_unbound_domain_svc
def update(unbound_domain_svc: UnboundDomainFacade, **kwargs):
    """
    Update a domain.
    """
    json_payload = {
        'domain': {}
    }
    options = ['enabled', 'domain', 'server', 'description']
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['domain'][option] = kwargs[option.lower()]

    result = unbound_domain_svc.update_domain(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@domain.command()
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
@pass_unbound_domain_svc
def delete(unbound_domain_svc: UnboundDomainFacade, **kwargs):
    """
    Delete domain
    """
    result = unbound_domain_svc.delete_domain(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
