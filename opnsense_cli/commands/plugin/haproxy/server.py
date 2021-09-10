import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats, int_as_string, tuple_to_csv
from opnsense_cli.commands.plugin.haproxy import haproxy
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.haproxy import Settings, Service
from opnsense_cli.facades.commands.plugin.haproxy.server import HaproxyServerFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_haproxy_server_svc = click.make_pass_decorator(HaproxyServerFacade)


@haproxy.group()
@pass_api_client
@click.pass_context
def server(ctx, api_client: ApiClient, **kwargs):
    """
    Server which serves content.
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = HaproxyServerFacade(settings_api, service_api)


@server.command()
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
        "uuid,enabled,name,type,address,port,description,ssl,sslVerify,weight"
    ),
    show_default=True,
)
@pass_haproxy_server_svc
def list(haproxy_server_svc: HaproxyServerFacade, **kwargs):
    """
    Show all server
    """
    result = haproxy_server_svc.list_servers()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@server.command()
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
        "enabled,name,description,address,port,checkport,mode,type,serviceName,number,"
        "linkedResolver,resolverOpts,resolvePrefer,ssl,sslVerify,sslCA,sslCRL,sslClientCertificate,"
        "weight,checkInterval,checkDownInterval,source,advanced"
    ),
    show_default=True,
)
@pass_haproxy_server_svc
def show(haproxy_server_svc: HaproxyServerFacade, **kwargs):
    """
    Show details for server
    """
    result = haproxy_server_svc.show_server(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@server.command()
@click.argument('name')
@click.option(
    '--enabled/--no-enabled',
    help='Enable or disable server.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--description', '-d',
    help='The server description.',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--address', '-a',
    help='The FQDN or the IP address of this server.',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--port', '-p',
    help=(
            'Provide the TCP or UDP communication port for this server. '
            'If unset, the same port the client connected to will be used'
    ),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--checkport', '--cp',
    help="Provide the TCP communication port to use during check.",
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--mode', '-m',
    help='Sets the operation mode to use for this server.',
    type=click.Choice(['', 'active', 'backup', 'disabled']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='active',
    required=False,
)
@click.option(
    '--type', '-t',
    help='The server type. Either static server or template to initialize multiple servers with shared parameters',
    type=click.Choice(['static', 'template']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='static',
    required=True,
)
@click.option(
    '--serviceName', '-sn',
    help=(
        'Provide either the FQDN for all the servers this template initializes or a service name to discover the '
        'available services via DNS SRV records.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--number', '-nu',
    help='The number of servers this template initializes, i.e. 5 or 1-5.',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--linkedResolver', '-lr',
    help=(
            'Specify the uuid of the resolver that the server template should look at '
            'to discover available services via DNS.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--resolverOpts', '-ro',
    help='Add resolver options.',
    type=click.Choice(['', 'allow-dup-ip', 'ignore-weight', 'prevent-dup-ip']),
    multiple=True,
    callback=tuple_to_csv,
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--resolvePrefer', '-rp',
    help=(
            'When DNS resolution is enabled for a server and multiple IP addresses from different families are returned, '
            'HAProxy will prefer using an IP address from the selected family.'
    ),
    type=click.Choice(['', 'ipv4', 'ipv6']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--ssl/--no-ssl',
    help='Enable or disable SSL communication with this server.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--sslVerify/--no-sslVerify',
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
    default=None,
    required=False,
)
@click.option(
    '--sslCRL', '-crl',
    help=(
            "This certificate revocation list Ids will be used to verify server's certificate. "
            "Pass multiple values comma separated"
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--sslClientCertificate', '-cert',
    help=(
            "This certificate will be sent if the server send a client certificate request. "
            "Pass the certificate id eg. 60cc4641eb577"
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--weight', '-w',
    help="Adjust the server's weight relative to other servers.",
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--checkInterval', '-ci',
    help="Sets the interval (in milliseconds) for running health checks on this server.",
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--checkDownInterval', '-cdi',
    help="Sets the interval (in milliseconds) for running health checks on the server when the server state is DOWN.",
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--source', '-s',
    help="Sets the source address which will be used when connecting to the server.",
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--advanced', '-adv',
    help=(
        "list of parameters that will be appended to the server line in every backend where this server will be used."
    ),
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
@pass_haproxy_server_svc
def create(haproxy_server_svc: HaproxyServerFacade, **kwargs):
    """
    Create a new server
    """
    json_payload = {
        'server': {
            "enabled": kwargs['enabled'],
            "name": kwargs['name'],
            "description": kwargs['description'],
            "address": kwargs['address'],
            "port": kwargs['port'],
            "checkport": kwargs['checkport'],
            "mode": kwargs['mode'],
            "type": kwargs['type'],
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

    result = haproxy_server_svc.create_server(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@server.command()
@click.argument('uuid')
@click.option(
    '--enabled/--no-enabled',
    help='Enable or disable server.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--name',
    help='The server name.',
    show_default=True,
    default=None
)
@click.option(
    '--description', '-d',
    help='The server description.',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--address', '-a',
    help='The FQDN or the IP address of this server.',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--port', '-p',
    help=(
        'Provide the TCP or UDP communication port for this server. '
        'If unset, the same port the client connected to will be used'
    ),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--checkport', '-cp',
    help="Provide the TCP communication port to use during check.",
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--mode', '-m',
    help='Sets the operation mode to use for this server.',
    type=click.Choice(['', 'active', 'backup', 'disabled']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='active',
    required=False,
)
@click.option(
    '--type', '-t',
    help='The server type. Either static server or template to initialize multiple servers with shared parameters',
    type=click.Choice(['static', 'template']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='static',
    required=True,
)
@click.option(
    '--serviceName', '-sn',
    help=(
            'Provide either the FQDN for all the servers this template initializes or a service name to discover the '
            'available services via DNS SRV records.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--number', '-nu',
    help='The number of servers this template initializes, i.e. 5 or 1-5.',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--linkedResolver', '-lr',
    help=(
            'Specify the uuid of the resolver that the server template should look at '
            'to discover available services via DNS.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--resolverOpts', '-ro',
    help='Add resolver options.',
    type=click.Choice(['', 'allow-dup-ip', 'ignore-weight', 'prevent-dup-ip']),
    multiple=True,
    callback=tuple_to_csv,
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--resolvePrefer', '-rp',
    help=(
            'When DNS resolution is enabled for a server and multiple IP addresses from different families are returned, '
            'HAProxy will prefer using an IP address from the selected family.'
    ),
    type=click.Choice(['', 'ipv4', 'ipv6']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--ssl/--no-ssl',
    help='Enable or disable SSL communication with this server.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--sslVerify/--no-sslVerify',
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
    default=None,
    required=False,
)
@click.option(
    '--sslCRL', '-crl',
    help=(
            "This certificate revocation list Ids will be used to verify server's certificate. "
            "Pass multiple values comma separated"
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--sslClientCertificate', '-cert',
    help=(
            "This certificate will be sent if the server send a client certificate request. "
            "Pass the certificate id eg. 60cc4641eb577"
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--weight', '-w',
    help="Adjust the server's weight relative to other servers.",
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--checkInterval', '-ci',
    help="Sets the interval (in milliseconds) for running health checks on this server.",
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--checkDownInterval', '-cdi',
    help="Sets the interval (in milliseconds) for running health checks on the server when the server state is DOWN.",
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--source', '-s',
    help="Sets the source address which will be used when connecting to the server.",
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--advanced', '-adv',
    help=(
            "list of parameters that will be appended to the server line in every backend where this server will be used."
    ),
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
@pass_haproxy_server_svc
def update(haproxy_server_svc: HaproxyServerFacade, **kwargs):
    """
    Update a server.
    """
    json_payload = {
        'server': {}
    }
    options = [
        'enabled', 'name', 'description', 'address', 'port', 'checkport', 'mode', 'type', 'serviceName',
        'number', 'linkedResolver', 'resolverOpts', 'resolvePrefer', 'ssl', 'sslVerify', 'sslCA', 'sslCRL',
        'sslClientCertificate', 'weight', 'checkInterval', 'checkDownInterval', 'source', 'advanced'
    ]
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['server'][option] = kwargs[option.lower()]

    result = haproxy_server_svc.update_server(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@server.command()
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
@pass_haproxy_server_svc
def delete(haproxy_server_svc: HaproxyServerFacade, **kwargs):
    """
    Delete server
    """
    result = haproxy_server_svc.delete_server(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
