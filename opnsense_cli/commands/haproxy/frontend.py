import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats, int_as_string
from opnsense_cli.commands.haproxy import haproxy
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.haproxy import Settings, Service
from opnsense_cli.facades.haproxy.frontend import HaproxyFrontendFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_haproxy_frontend_svc = click.make_pass_decorator(HaproxyFrontendFacade)


@haproxy.group()
@pass_api_client
@click.pass_context
def frontend(ctx, api_client: ApiClient, **kwargs):
    """
    Manage haproxy frontends

    See: https://docs.opnsense.org/manual/how-tos/haproxy.html#fifth-step-configure-a-frontend
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = HaproxyFrontendFacade(settings_api, service_api)


@frontend.command()
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
        "uuid,enabled,name,description,bind,mode,Backend,ssl_enabled"
    )
)
@pass_haproxy_frontend_svc
def list(haproxy_frontend_svc: HaproxyFrontendFacade, **kwargs):
    """
    Show all backends
    """
    result = haproxy_frontend_svc.list_frontends()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@frontend.command()
@click.argument('frontend_uuid')
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
    default="enabled,name,description,bind,mode,Backend,ssl_enabled",
    show_default=True,
)
@pass_haproxy_frontend_svc
def show(haproxy_frontend_svc: HaproxyFrontendFacade, **kwargs):
    """
    Show details for backend
    """
    result = haproxy_frontend_svc.show_frontend(kwargs['frontend_uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@frontend.command()
@click.argument('name_or_prefix')
@click.option(
    '--enabled/--disabled',
    help='Enable or disable server.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--type', '-t',
    help='The server type. Either static server or template to initialize multiple servers with shared parameters',
    type=click.Choice(['static', 'template']),
    show_default=True,
    required=True,
    default='static'
)
@click.option(
    '--description', '-d',
    help='The server description.',
    show_default=True,
)
@click.option(
    '--address', '-a',
    help='The FQDN or the IP address of this server.',
    show_default=True,
)
@click.option(
    '--serviceName', '-sn',
    help=(
            'Provide either the FQDN for all the servers this template initializes or a service name to discover the '
            'available services via DNS SRV records.'
    ),
    show_default=True,
)
@click.option(
    '--number', '-nu',
    help='The number of servers this template initializes, i.e. 5 or 1-5.',
    show_default=True,
)
@click.option(
    '--linkedResolver', '-lr',
    help=(
            'Specify the uuid of the resolver that the server template should look at '
            'to discover available services via DNS.'
    ),
    show_default=True,
)
@click.option(
    '--resolverOpts', '-ro',
    help='Add resolver options.',
    show_default=True,
)
@click.option(
    '--port', '-p',
    help=(
            'Provide the TCP or UDP communication port for this server. '
            'If unset, the same port the client connected to will be used'
    ),
    type=int,
    callback=int_as_string,
    show_default=True,
)
@click.option(
    '--mode', '-m',
    help='Sets the operation mode to use for this server.',
    type=click.Choice(['', 'active', 'backup', 'disabled']),
    show_default=True,
)
@click.option(
    '--resolvePrefer', '-rp',
    help=(
            'When DNS resolution is enabled for a server and multiple IP addresses from different families are returned, '
            'HAProxy will prefer using an IP address from the selected family.'
    ),
    type=click.Choice(['', 'ipv4', 'ipv6']),
    show_default=True,
)
@click.option(
    '--ssl/--no-ssl',
    help='Enable or disable SSL communication with this server.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=False,
    required=True,
)
@click.option(
    '--sslVerify/--no-sslVerify', '--ssl-verify/--no-ssl-verify',
    help='Enable or disable server ssl certificate verification.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--sslCA', '-ca',
    help="These CA Ids will be used to verify server's certificate. Pass multiple values comma separated",
    show_default=True,
)
@click.option(
    '--sslCRL', '-crl',
    help=(
            "This certificate revocation list Ids will be used to verify server's certificate. "
            "Pass multiple values comma separated"
    ),
    show_default=True,
)
@click.option(
    '--sslClientCertificate', '-cert',
    help=(
            "This certificate will be sent if the server send a client certificate request. "
            "Pass the certificate id eg. 60cc4641eb577"
    ),
    show_default=True,
)
@click.option(
    '--weight', '-w',
    help="Adjust the server's weight relative to other servers.",
    type=int,
    callback=int_as_string,
)
@click.option(
    '--checkInterval', '-ci',
    help="Sets the interval (in milliseconds) for running health checks on this server.",
    type=int,
    callback=int_as_string,
)
@click.option(
    '--checkDownInterval', '-cdi',
    help="Sets the interval (in milliseconds) for running health checks on the server when the server state is DOWN.",
    type=int,
    callback=int_as_string,
)
@click.option(
    '--checkport', '-cp',
    help="Provide the TCP communication port to use during check.",
    type=int,
    callback=int_as_string,
)
@click.option(
    '--source', '-s',
    help="Sets the source address which will be used when connecting to the server..",
    show_default=True,
)
@click.option(
    '--advanced', '-opt',
    help=(
            "list of parameters that will be appended to the server line in every backend where this server will be used."
    ),
    show_default=True,
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
@pass_haproxy_frontend_svc
def create(haproxy_frontend_svc: HaproxyFrontendFacade, **kwargs):
    """
    Create a new backend
    """
    json_payload = {
        'frontend': {
            "enabled": kwargs['enabled'],
            "name": kwargs['name_or_prefix'],
            "description": kwargs['description'],
            "type": kwargs['type'],
            "address": kwargs['address'],
            "port": kwargs['port'],
            "checkport": kwargs['checkport'],
            "mode": kwargs['mode'],
            "serviceName": kwargs['servicename'],
            "number": kwargs['number'],
            "linkedResolver": kwargs['linkedresolver'],
            "resolverOpts": kwargs['resolveropts'],
            "resolvePrefer": kwargs['resolveprefer'],
            "ssl": kwargs['ssl'],
            "sslVerify": kwargs['sslverify'],
            "sslCA": kwargs['sslca'],
            "sslCRL": kwargs['sslcrl'],
            "sslClientCertificate": kwargs['sslclientcertificate'],
            "weight": kwargs['weight'],
            "checkInterval": kwargs['checkinterval'],
            "checkDownInterval": kwargs['checkdowninterval'],
            "source": kwargs['source'],
            "advanced": kwargs['advanced'],
        }
    }

    result = haproxy_frontend_svc.create_frontend(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@frontend.command()
@click.argument('frontend_uuid')
@click.option(
    '--name', '-n',
    help='The server name.',
    show_default=True,
)
@click.option(
    '--enabled/--disabled',
    help='Enable or disable server.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None,
)
@click.option(
    '--type', '-t',
    help='The server type. Either static server or template to initialize multiple servers with shared parameters',
    type=click.Choice(['static', 'template']),
    show_default=True,
)
@click.option(
    '--description', '-d',
    help='The server description.',
    show_default=True,
)
@click.option(
    '--address', '-a',
    help='The FQDN or the IP address of this server.',
    show_default=True,
)
@click.option(
    '--serviceName', '-sn',
    help=(
            'Provide either the FQDN for all the servers this template initializes or a service name to discover the '
            'available services via DNS SRV records.'
    ),
    show_default=True,
)
@click.option(
    '--number', '-num',
    help='The number of servers this template initializes, i.e. 5 or 1-5.',
    show_default=True,
)
@click.option(
    '--linkedResolver', '-lr',
    help=(
            'Specify the uuid of the resolver that the server template should look at '
            'to discover available services via DNS.'
    ),
    show_default=True,
)
@click.option(
    '--resolverOpts', '-ro',
    help='Add resolver options.',
    show_default=True,
)
@click.option(
    '--port', '-p',
    help=(
            'Provide the TCP or UDP communication port for this server. '
            'If unset, the same port the client connected to will be used'
    ),
    type=int,
    callback=int_as_string,
    show_default=True,
)
@click.option(
    '--mode', '-m',
    help='Sets the operation mode to use for this server.',
    type=click.Choice(['', 'active', 'backup', 'disabled']),
    show_default=True,
)
@click.option(
    '--resolvePrefer', '-rp',
    help=(
            'When DNS resolution is enabled for a server and multiple IP addresses from different families are returned, '
            'HAProxy will prefer using an IP address from the selected family.'
    ),
    type=click.Choice(['', 'ipv4', 'ipv6']),
    show_default=True,
)
@click.option(
    '--ssl/--no-ssl',
    help='Enable or disable SSL communication with this server.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None,
)
@click.option(
    '--sslVerify/--no-sslVerify', '--ssl-verify/--no-ssl-verify',
    help='Enable or disable server ssl certificate verification.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None,
)
@click.option(
    '--sslCA', '-ca',
    help="These CA Ids will be used to verify server's certificate. Pass multiple values comma separated",
    show_default=True,
)
@click.option(
    '--sslCRL', '-crl',
    help=(
            "This certificate revocation list Ids will be used to verify server's certificate. "
            "Pass multiple values comma separated"
    ),
    show_default=True,
)
@click.option(
    '--sslClientCertificate', '-cert',
    help=(
            "This certificate will be sent if the server send a client certificate request. "
            "Pass the certificate id eg. 60cc4641eb577"
    ),
    show_default=True,
)
@click.option(
    '--weight', '-w',
    help="Adjust the server's weight relative to other servers.",
    type=int,
    callback=int_as_string,
)
@click.option(
    '--checkInterval', '-ci',
    help="Sets the interval (in milliseconds) for running health checks on this server.",
    type=int,
    callback=int_as_string,
)
@click.option(
    '--checkDownInterval', '-cdi',
    help="Sets the interval (in milliseconds) for running health checks on the server when the server state is DOWN.",
    type=int,
    callback=int_as_string,
)
@click.option(
    '--checkport', '-cp',
    help="Provide the TCP communication port to use during check.",
    type=int,
    callback=int_as_string,
)
@click.option(
    '--source', '-s',
    help="Sets the source address which will be used when connecting to the server..",
    show_default=True,
)
@click.option(
    '--advanced', '-opt',
    help=(
            "list of parameters that will be appended to the server line in every backend where this server will be used."
    ),
    show_default=True,
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
@pass_haproxy_frontend_svc
def update(haproxy_frontend_svc: HaproxyFrontendFacade, **kwargs):
    """
    Update frontend
    """
    json_payload = {
        'frontend': {}
    }
    options = [
        'enabled', 'name', 'description', 'address', 'port', 'checkport', 'mode', 'type', 'serviceName', 'number',
        'linkedresolver', 'resolverOpts', 'resolvePrefer', 'ssl', 'sslVerify', 'sslCA', 'sslCRL',
        'sslClientCertificate', 'weight', 'checkInterval', 'checkDownInterval', 'source', 'advanced'
    ]
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['frontend'][option] = kwargs[option.lower()]

    result = haproxy_frontend_svc.update_frontend(kwargs['frontend_uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@frontend.command()
@click.argument('frontend_uuid')
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
@pass_haproxy_frontend_svc
def delete(haproxy_frontend_svc: HaproxyFrontendFacade, **kwargs):
    """
    Delete a backend
    """
    result = haproxy_frontend_svc.delete_frontend(kwargs['frontend_uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
