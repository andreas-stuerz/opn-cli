import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats, resolve_linked_names_to_uuids
from opnsense_cli.commands.core.unbound import unbound
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.core.unbound import Settings, Service
from opnsense_cli.facades.commands.core.unbound.alias import UnboundAliasFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_unbound_alias_svc = click.make_pass_decorator(UnboundAliasFacade)


@unbound.group()
@pass_api_client
@click.pass_context
def alias(ctx, api_client: ApiClient, **kwargs):
    """
    Manage unbound host alias overrides
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = UnboundAliasFacade(settings_api, service_api)


@alias.command()
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
        "uuid,enabled,Host,hostname,domain,description"
    ),
    show_default=True,
)
@pass_unbound_alias_svc
def list(unbound_alias_svc: UnboundAliasFacade, **kwargs):
    """
    Show all alias
    """
    result = unbound_alias_svc.list_aliass()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@alias.command()
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
        "enabled,host,hostname,domain,description"
    ),
    show_default=True,
)
@pass_unbound_alias_svc
def show(unbound_alias_svc: UnboundAliasFacade, **kwargs):
    """
    Show details for alias
    """
    result = unbound_alias_svc.show_alias(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@alias.command()
@click.option(
    '--enabled/--no-enabled',
    help=('Enable this alias for the selected host'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--host',
    help=(
        'The associated host to apply this alias on. Use an uuid or a name reference "hostname_domain_rr_mxprio_mx_server" '
        'e.g. "myhost_example.com_A___10.0.0.1" or "mx_example.com_MX_10_mailin.example.com"'
    ),
    callback=resolve_linked_names_to_uuids,
    show_default=True,
    default=None,
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
@pass_unbound_alias_svc
def create(unbound_alias_svc: UnboundAliasFacade, **kwargs):
    """
    Create a new alias
    """
    json_payload = {
        'alias': {
            "enabled": kwargs['enabled'],
            "host": kwargs['host'],
            "hostname": kwargs['hostname'],
            "domain": kwargs['domain'],
            "description": kwargs['description'],
        }
    }

    result = unbound_alias_svc.create_alias(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@alias.command()
@click.argument('uuid')
@click.option(
    '--enabled/--no-enabled',
    help=('Enable this alias for the selected host'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--host',
    help=(
        'The associated host to apply this alias on. Use an uuid or a name reference "hostname_domain_rr_mxprio_mx_server" '
        'e.g. "myhost_example.com_A___10.0.0.1" or "mx_example.com_MX_10_mailin.example.com"'
    ),
    callback=resolve_linked_names_to_uuids,
    show_default=True,
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
@pass_unbound_alias_svc
def update(unbound_alias_svc: UnboundAliasFacade, **kwargs):
    """
    Update an alias.
    """
    json_payload = {
        'alias': {}
    }
    options = ['enabled', 'host', 'hostname', 'domain', 'description']
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['alias'][option] = kwargs[option.lower()]

    result = unbound_alias_svc.update_alias(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@alias.command()
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
@pass_unbound_alias_svc
def delete(unbound_alias_svc: UnboundAliasFacade, **kwargs):
    """
    Delete alias
    """
    result = unbound_alias_svc.delete_alias(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
