import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats, int_as_string
from opnsense_cli.commands.plugin.haproxy import haproxy
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.haproxy import Settings, Service
from opnsense_cli.facades.commands.plugin.haproxy.resolver import HaproxyResolverFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_haproxy_resolver_svc = click.make_pass_decorator(HaproxyResolverFacade)


@haproxy.group()
@pass_api_client
@click.pass_context
def resolver(ctx, api_client: ApiClient, **kwargs):
    """
    Individual name resolution configurations for backends.

    This feature allows in-depth configuration of how HAProxy handles name resolution and interacts with
    name resolvers (DNS). Each resolver configuration can be used in Backend Pools to apply individual
    name resolution configurations.
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = HaproxyResolverFacade(settings_api, service_api)


@resolver.command()
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
        "uuid,enabled,name,description,nameservers,parse_resolv_conf,resolve_retries,timeout_resolve,timeout_retry"
    ),
    show_default=True,
)
@pass_haproxy_resolver_svc
def list(haproxy_resolver_svc: HaproxyResolverFacade, **kwargs):
    """
    Show all resolver
    """
    result = haproxy_resolver_svc.list_resolvers()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@resolver.command()
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
        "enabled,name,description,nameservers,parse_resolv_conf,resolve_retries,timeout_resolve,timeout_retry"
    ),
    show_default=True,
)
@pass_haproxy_resolver_svc
def show(haproxy_resolver_svc: HaproxyResolverFacade, **kwargs):
    """
    Show details for resolver
    """
    result = haproxy_resolver_svc.show_resolver(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@resolver.command()
@click.argument('name')
@click.option(
    '--enabled/--no-enabled',
    help=('Enable this resolver configuration.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--description',
    help=('Choose a optional description for this resolver configuration.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--nameservers',
    help=(
        'Add nameservers to this resolver configuration, i.e. 127.0.0.1:53 or 192.168.1.1:53.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--parse_resolv_conf/--no-parse_resolv_conf',
    help=('Add all nameservers found in /etc/resolv.conf to this resolver configuration.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--resolve_retries',
    help=('This configures the number of queries to send to resolve a server name before giving up.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=3,
    required=False,
)
@click.option(
    '--timeout_resolve',
    help=(
        'This configures the default time to trigger name resolutions when no other time applied. '
        'Enter a number followed by one of the supported suffixes '
        '"d" (days), "h" (hour), "m" (minute), "s" (seconds), "ms" (miliseconds).'
    ),
    show_default=True,
    default='1s',
    required=False,
)
@click.option(
    '--timeout_retry',
    help=(
        'This configures the default time between two DNS queries, when no valid response has been received. '
        'Enter a number followed by one of the supported suffixes '
        '"d" (days), "h" (hour), "m" (minute), "s" (seconds), "ms" (miliseconds).'
    ),
    show_default=True,
    default='1s',
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
@pass_haproxy_resolver_svc
def create(haproxy_resolver_svc: HaproxyResolverFacade, **kwargs):
    """
    Create a new resolver
    """
    json_payload = {
        'resolver': {
            "enabled": kwargs['enabled'],
            "name": kwargs['name'],
            "description": kwargs['description'],
            "nameservers": kwargs['nameservers'],
            "parse_resolv_conf": kwargs['parse_resolv_conf'],
            "resolve_retries": kwargs['resolve_retries'],
            "timeout_resolve": kwargs['timeout_resolve'],
            "timeout_retry": kwargs['timeout_retry'],
        }
    }

    result = haproxy_resolver_svc.create_resolver(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@resolver.command()
@click.argument('uuid')
@click.option(
    '--enabled/--no-enabled',
    help=('Enable this resolver configuration.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--name',
    help=('Choose a name for this resolver configuration.'),
    show_default=True,
    default=None
)
@click.option(
    '--description',
    help=('Choose a optional description for this resolver configuration.'),
    show_default=True,
    default=None
)
@click.option(
    '--nameservers',
    help=(
        'Add nameservers to this resolver configuration, i.e. 127.0.0.1:53 or 192.168.1.1:53.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--parse_resolv_conf/--no-parse_resolv_conf',
    help=('Add all nameservers found in /etc/resolv.conf to this resolver configuration.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--resolve_retries',
    help=('This configures the number of queries to send to resolve a server name before giving up.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--timeout_resolve',
    help=(
        'This configures the default time to trigger name resolutions when no other time applied. '
        'Enter a number followed by one of the supported suffixes '
        '"d" (days), "h" (hour), "m" (minute), "s" (seconds), "ms" (miliseconds).'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--timeout_retry',
    help=(
        'This configures the default time between two DNS queries, when no valid response has been received. '
        'Enter a number followed by one of the supported suffixes '
        '"d" (days), "h" (hour), "m" (minute), "s" (seconds), "ms" (miliseconds).'
    ),
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
@pass_haproxy_resolver_svc
def update(haproxy_resolver_svc: HaproxyResolverFacade, **kwargs):
    """
    Update a resolver.
    """
    json_payload = {
        'resolver': {}
    }
    options = [
        'enabled', 'name', 'description', 'nameservers', 'parse_resolv_conf', 'resolve_retries', 'timeout_resolve',
        'timeout_retry'
    ]
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['resolver'][option] = kwargs[option.lower()]

    result = haproxy_resolver_svc.update_resolver(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@resolver.command()
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
@pass_haproxy_resolver_svc
def delete(haproxy_resolver_svc: HaproxyResolverFacade, **kwargs):
    """
    Delete resolver
    """
    result = haproxy_resolver_svc.delete_resolver(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
