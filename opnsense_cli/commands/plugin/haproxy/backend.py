import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats, int_as_string, tuple_to_csv
from opnsense_cli.commands.plugin.haproxy import haproxy
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.haproxy import Settings, Service
from opnsense_cli.facades.commands.plugin.haproxy.backend import HaproxyBackendFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_haproxy_backend_svc = click.make_pass_decorator(HaproxyBackendFacade)


@haproxy.group()
@pass_api_client
@click.pass_context
def backend(ctx, api_client: ApiClient, **kwargs):
    """
    Health monitoring and load distribution for servers.
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = HaproxyBackendFacade(settings_api, service_api)


@backend.command()
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
        "uuid,enabled,name,description,mode,algorithm,Servers,"
        "healthCheckEnabled,Healthcheck,persistence,stickiness_pattern"
    )
)
@pass_haproxy_backend_svc
def list(haproxy_backend_svc: HaproxyBackendFacade, **kwargs):
    """
    Show all backend
    """
    result = haproxy_backend_svc.list_backends()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@backend.command()
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
        "enabled,name,description,mode,algorithm,random_draws,proxyProtocol,linkedServers,"
        "linkedResolver,resolverOpts,resolvePrefer,source,"
        "healthCheckEnabled,healthCheck,healthCheckLogStatus,checkInterval,checkDownInterval,"
        "healthCheckFall,healthCheckRise,linkedMailer,http2Enabled,http2Enabled_nontls,"
        "ba_advertised_protocols,persistence,persistence_cookiemode,persistence_cookiename,"
        "persistence_stripquotes,stickiness_pattern,stickiness_dataTypes,stickiness_expire,"
        "stickiness_size,stickiness_cookiename,stickiness_cookielength,stickiness_connRatePeriod,"
        "stickiness_sessRatePeriod,stickiness_httpReqRatePeriod,stickiness_httpErrRatePeriod,"
        "stickiness_bytesInRatePeriod,stickiness_bytesOutRatePeriod,basicAuthEnabled,basicAuthUsers,"
        "basicAuthGroups,tuning_timeoutConnect,tuning_timeoutCheck,tuning_timeoutServer,"
        "tuning_retries,customOptions,tuning_defaultserver,tuning_noport,tuning_httpreuse,tuning_caching,"
        "linkedActions,linkedErrorfiles"
    ),
    show_default=True,
)
@pass_haproxy_backend_svc
def show(haproxy_backend_svc: HaproxyBackendFacade, **kwargs):
    """
    Show details for backend
    """
    result = haproxy_backend_svc.show_backend(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@backend.command()
@click.argument('name')
@click.option(
    '--enabled/--no-enabled',
    help='Enable or disable this backend.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--description',
    help='Description for this backend pool.',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--mode',
    help='Set the running mode or protocol of the backend pool.',
    type=click.Choice(['http', 'tcp']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='http',
    required=True,
)
@click.option(
    '--algorithm',
    help='Define the load balancing algorithm to be used in a backend pool.',
    type=click.Choice(['source', 'roundrobin', 'static-rr', 'leastconn', 'uri', 'random']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='source',
    required=True,
)
@click.option(
    '--random_draws',
    help=(
        'When using the Random Balancing Algorithm, this value indicates the number of draws '
        'before selecting the least loaded of these servers.'
    ),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=2,
    required=True,
)
@click.option(
    '--proxyProtocol',
    help='Enforces use of the PROXY protocol over any connection established to the configured servers.',
    type=click.Choice(['', 'v1', 'v2']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--linkedServers',
    help='Add servers to this backend.',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--linkedResolver',
    help='Select the custom resolver configuration that should be used for all servers in this backend.',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--resolverOpts',
    help='Add resolver options.',
    type=click.Choice(['', 'allow-dup-ip', 'ignore-weight', 'prevent-dup-ip']),
    multiple=True,
    callback=tuple_to_csv,
    show_default=True,
    default=[],
    required=False,
)
@click.option(
    '--resolvePrefer',
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
    '--source',
    help='Sets the source address which will be used when connecting to the server(s).',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--healthCheckEnabled/--no-healthCheckEnabled',
    help='Enable or disable health checking.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--healthCheck',
    help='Select health check for servers in this backend.',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--healthCheckLogStatus/--no-healthCheckLogStatus',
    help='Enable to log health check status updates.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--checkInterval',
    help=(
        'Sets the interval (in milliseconds) for running health checks on all configured servers. '
        'This setting takes precedence over default values in health monitors and real servers.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--checkDownInterval',
    help=(
        'Sets the interval (in milliseconds) for running health checks on a configured server when the server state '
        'is DOWN. If it is not set HAProxy uses the check interval.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--healthCheckFall',
    help='The number of consecutive unsuccessful health checks before a server is considered as unavailable.',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--healthCheckRise',
    help='The number of consecutive successful health checks before a server is considered as available.',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--linkedMailer',
    help='Select an e-mail alert configuration. An e-mail is sent when the state of a server changes.',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http2Enabled/--no-http2Enabled',
    help='Enable support for end-to-end HTTP/2 communication.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--http2Enabled_nontls/--no-http2Enabled_nontls',
    help='Enable support for HTTP/2 even if TLS is not enabled.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--ba_advertised_protocols',
    help=(
        'When using the TLS ALPN extension, HAProxy advertises the specified protocol list as supported on top of ALPN.'
        ' TLS must be enabled.'
    ),
    type=click.Choice(['', 'h2', 'http11', 'http10']),
    multiple=True,
    callback=tuple_to_csv,
    show_default=True,
    default=['h2', 'http11'],
    required=False,
)
@click.option(
    '--persistence',
    help=(
        'Choose how HAProxy should track user-to-server mappings. '
        'Stick-table persistence works with all protocols, but is broken in multi-process and multithreaded modes. '
        'Cookie-based persistence only works with HTTP/HTTPS protocols.'
    ),
    type=click.Choice(['', 'sticktable', 'cookie']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='sticktable',
    required=False,
)
@click.option(
    '--persistence_cookiemode',
    help=(
        'Usually it is better to reuse an existing cookie. '
        'In this case HAProxy prefixes the cookie with the required information.'
    ),
    type=click.Choice(['piggyback', 'new']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='piggyback',
    required=True,
)
@click.option(
    '--persistence_cookiename',
    help='Cookie name to use for persistence.',
    show_default=True,
    default='SRVCOOKIE',
    required=False,
)
@click.option(
    '--persistence_stripquotes/--no-persistence_stripquotes',
    help='Enable to automatically strip quotes from the cookie value.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--stickiness_pattern',
    help='Choose a request pattern to associate a user to a server.',
    type=click.Choice(['', 'sourceipv4', 'sourceipv6', 'cookievalue', 'rdpcookie']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='sourceipv4',
    required=False,
)
@click.option(
    '--stickiness_dataTypes',
    help=(
        'This is used to store additional information in the stick-table. '
        'It may be used by ACLs in order to control various criteria related to the activity of the client matching '
        'the stick-table. Note that this directly impacts memory usage.'
    ),
    type=click.Choice(
        [
            '', 'conn_cnt', 'conn_cur', 'conn_rate', 'sess_cnt', 'sess_rate', 'http_req_cnt', 'http_req_rate',
            'http_err_cnt', 'http_err_rate', 'bytes_in_cnt', 'bytes_in_rate', 'bytes_out_cnt', 'bytes_out_rate'
        ]
    ),
    multiple=True,
    callback=tuple_to_csv,
    show_default=True,
    default=[],
    required=False,
)
@click.option(
    '--stickiness_expire',
    help=(
        'This configures the maximum duration of an entry in the stick-table since it was last created, refreshed '
        'or matched. The maximum duration is slightly above 24 days. Enter a number followed by one of the supported '
        'suffixes "d" (days), "h" (hour), "m" (minute), "s" (seconds), "ms" (miliseconds).'
    ),
    show_default=True,
    default='30m',
    required=True,
)
@click.option(
    '--stickiness_size',
    help=(
        'This configures the maximum number of entries that can fit in the table. '
        'This value directly impacts memory usage. '
        'Count approximately 50 bytes per entry, plus the size of a string if any. '
        'Enter a number followed by one of the supported suffixes "k", "m", "g".'
    ),
    show_default=True,
    default='50k',
    required=True,
)
@click.option(
    '--stickiness_cookiename',
    help='Cookie name to use for stick table.',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--stickiness_cookielength',
    help='The maximum number of characters that will be stored in the stick table.',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--stickiness_connRatePeriod',
    help=(
        'The length of the period over which the average is measured. It reports the average incoming connection rate '
        'over that period, in connections per period. Defaults to milliseconds. '
        'Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default='10s',
    required=False,
)
@click.option(
    '--stickiness_sessRatePeriod',
    help=(
        'The length of the period over which the average is measured. '
        'It reports the average incoming session rate over that period, '
        'in sessions per period. Defaults to milliseconds. '
        'Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default='10s',
    required=False,
)
@click.option(
    '--stickiness_httpReqRatePeriod',
    help=(
        'The length of the period over which the average is measured. '
        'It reports the average HTTP request rate over that period, in requests per period. '
        'Defaults to milliseconds. Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default='10s',
    required=False,
)
@click.option(
    '--stickiness_httpErrRatePeriod',
    help=(
        'The length of the period over which the average is measured. '
        'It reports the average HTTP request error rate over that period, in requests per period. '
        'Defaults to milliseconds. Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default='10s',
    required=False,
)
@click.option(
    '--stickiness_bytesInRatePeriod',
    help=(
        'The length of the period over which the average is measured. '
        'It reports the average incoming bytes rate over that period, in bytes per period. Defaults to milliseconds. '
        'Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default='1m',
    required=False,
)
@click.option(
    '--stickiness_bytesOutRatePeriod',
    help=(
        'The length of the period over which the average is measured. '
        'It reports the average outgoing bytes rate over that period, in bytes per period. '
        'Defaults to milliseconds. Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default='1m',
    required=False,
)
@click.option(
    '--basicAuthEnabled/--no-basicAuthEnabled',
    help='Enable HTTP basic authentication.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--basicAuthUsers',
    help='Basic auth users.',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--basicAuthGroups',
    help='Basic auth groups.',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tuning_timeoutConnect',
    help=(
        'Set the maximum time to wait for a connection attempt to a server to succeed. '
        'Defaults to milliseconds. Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tuning_timeoutCheck',
    help=(
        'Sets an additional read timeout for running health checks on a server. '
        'Defaults to milliseconds. Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tuning_timeoutServer',
    help=(
        'Set the maximum inactivity time on the server side. Defaults to milliseconds. '
        'Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tuning_retries',
    help=(
        'Set the number of retries to perform on a server after a connection failure.'
    ),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--customOptions',
    help=(
        'These lines will be added to the HAProxy backend configuration.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tuning_defaultserver',
    help=(
        'Default option for all server entries.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tuning_noport/--no-tuning_noport',
    help=(
        "Don't use port on server, use the same port as frontend receive. "
        "If check enable, require port check in server."
    ),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--tuning_httpreuse',
    help=(
        'Declare how idle HTTP connections may be shared between requests.'
    ),
    type=click.Choice(['', 'never', 'safe', 'aggressive', 'always']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='safe',
    required=False,
)
@click.option(
    '--tuning_caching/--no-tuning_caching',
    help=(
        'Enable caching of responses from this backend. '
        'The HAProxy cache must be enabled under Settings before this will have any effect.'
    ),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--linkedActions',
    help='Choose rules to be included in this backend pool.',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--linkedErrorfiles',
    help='Choose error messages to be included in this backend pool.',
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
@pass_haproxy_backend_svc
def create(haproxy_backend_svc: HaproxyBackendFacade, **kwargs):
    """
    Create a new backend
    """
    json_payload = {
        'backend': {
            "enabled": kwargs['enabled'],
            "name": kwargs['name'],
            "description": kwargs['description'],
            "mode": kwargs['mode'],
            "algorithm": kwargs['algorithm'],
            "random_draws": kwargs['random_draws'],
            "proxyProtocol": kwargs['proxyprotocol'],
            "linkedServers": kwargs['linkedservers'],
            "linkedResolver": kwargs['linkedresolver'],
            "resolverOpts": kwargs['resolveropts'],
            "resolvePrefer": kwargs['resolveprefer'],
            "source": kwargs['source'],
            "healthCheckEnabled": kwargs['healthcheckenabled'],
            "healthCheck": kwargs['healthcheck'],
            "healthCheckLogStatus": kwargs['healthchecklogstatus'],
            "checkInterval": kwargs['checkinterval'],
            "checkDownInterval": kwargs['checkdowninterval'],
            "healthCheckFall": kwargs['healthcheckfall'],
            "healthCheckRise": kwargs['healthcheckrise'],
            "linkedMailer": kwargs['linkedmailer'],
            "http2Enabled": kwargs['http2enabled'],
            "http2Enabled_nontls": kwargs['http2enabled_nontls'],
            "ba_advertised_protocols": kwargs['ba_advertised_protocols'],
            "persistence": kwargs['persistence'],
            "persistence_cookiemode": kwargs['persistence_cookiemode'],
            "persistence_cookiename": kwargs['persistence_cookiename'],
            "persistence_stripquotes": kwargs['persistence_stripquotes'],
            "stickiness_pattern": kwargs['stickiness_pattern'],
            "stickiness_dataTypes": kwargs['stickiness_datatypes'],
            "stickiness_expire": kwargs['stickiness_expire'],
            "stickiness_size": kwargs['stickiness_size'],
            "stickiness_cookiename": kwargs['stickiness_cookiename'],
            "stickiness_cookielength": kwargs['stickiness_cookielength'],
            "stickiness_connRatePeriod": kwargs['stickiness_connrateperiod'],
            "stickiness_sessRatePeriod": kwargs['stickiness_sessrateperiod'],
            "stickiness_httpReqRatePeriod": kwargs['stickiness_httpreqrateperiod'],
            "stickiness_httpErrRatePeriod": kwargs['stickiness_httperrrateperiod'],
            "stickiness_bytesInRatePeriod": kwargs['stickiness_bytesinrateperiod'],
            "stickiness_bytesOutRatePeriod": kwargs['stickiness_bytesoutrateperiod'],
            "basicAuthEnabled": kwargs['basicauthenabled'],
            "basicAuthUsers": kwargs['basicauthusers'],
            "basicAuthGroups": kwargs['basicauthgroups'],
            "tuning_timeoutConnect": kwargs['tuning_timeoutconnect'],
            "tuning_timeoutCheck": kwargs['tuning_timeoutcheck'],
            "tuning_timeoutServer": kwargs['tuning_timeoutserver'],
            "tuning_retries": kwargs['tuning_retries'],
            "customOptions": kwargs['customoptions'],
            "tuning_defaultserver": kwargs['tuning_defaultserver'],
            "tuning_noport": kwargs['tuning_noport'],
            "tuning_httpreuse": kwargs['tuning_httpreuse'],
            "tuning_caching": kwargs['tuning_caching'],
            "linkedActions": kwargs['linkedactions'],
            "linkedErrorfiles": kwargs['linkederrorfiles'],

        }
    }

    result = haproxy_backend_svc.create_backend(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@backend.command()
@click.argument('uuid')
@click.option(
    '--enabled/--no-enabled',
    help='Enable or disable this backend.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--name',
    help='The name of the backend pool.',
    show_default=True,
    default=None
)
@click.option(
    '--description',
    help='Description for this backend pool.',
    show_default=True,
    default=None
)
@click.option(
    '--mode',
    help='Set the running mode or protocol of the backend pool.',
    type=click.Choice(['http', 'tcp']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--algorithm',
    help='Define the load balancing algorithm to be used in a backend pool.',
    type=click.Choice(['source', 'roundrobin', 'static-rr', 'leastconn', 'uri', 'random']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--random_draws',
    help=(
        'When using the Random Balancing Algorithm, this value indicates the number of draws '
        'before selecting the least loaded of these servers.'
    ),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--proxyProtocol',
    help='Enforces use of the PROXY protocol over any connection established to the configured servers.',
    type=click.Choice(['', 'v1', 'v2']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--linkedServers',
    help='Add servers to this backend.',
    show_default=True,
    default=None
)
@click.option(
    '--linkedResolver',
    help='Select the custom resolver configuration that should be used for all servers in this backend.',
    show_default=True,
    default=None
)
@click.option(
    '--resolverOpts',
    help='Add resolver options.',
    type=click.Choice(['', 'allow-dup-ip', 'ignore-weight', 'prevent-dup-ip']),
    multiple=True,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--resolvePrefer',
    help=(
        'When DNS resolution is enabled for a server and multiple IP addresses from different families are returned, '
        'HAProxy will prefer using an IP address from the selected family.'
    ),
    type=click.Choice(['', 'ipv4', 'ipv6']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--source',
    help='Sets the source address which will be used when connecting to the server(s).',
    show_default=True,
    default=None
)
@click.option(
    '--healthCheckEnabled/--no-healthCheckEnabled',
    help='Enable or disable health checking.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--healthCheck',
    help='Select health check for servers in this backend.',
    show_default=True,
    default=None
)
@click.option(
    '--healthCheckLogStatus/--no-healthCheckLogStatus',
    help='Enable to log health check status updates.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--checkInterval',
    help=(
        'Sets the interval (in milliseconds) for running health checks on all configured servers. '
        'This setting takes precedence over default values in health monitors and real servers.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--checkDownInterval',
    help=(
        'Sets the interval (in milliseconds) for running health checks on a configured server when the server state '
        'is DOWN. If it is not set HAProxy uses the check interval.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--healthCheckFall',
    help='The number of consecutive unsuccessful health checks before a server is considered as unavailable.',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--healthCheckRise',
    help='The number of consecutive successful health checks before a server is considered as available.',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--linkedMailer',
    help='Select an e-mail alert configuration. An e-mail is sent when the state of a server changes.',
    show_default=True,
    default=None
)
@click.option(
    '--http2Enabled/--no-http2Enabled',
    help='Enable support for end-to-end HTTP/2 communication.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--http2Enabled_nontls/--no-http2Enabled_nontls',
    help='Enable support for HTTP/2 even if TLS is not enabled.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--ba_advertised_protocols',
    help=(
        'When using the TLS ALPN extension, HAProxy advertises the specified protocol list as supported on top of ALPN.'
        ' TLS must be enabled.'
    ),
    type=click.Choice(['', 'h2', 'http11', 'http10']),
    multiple=True,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--persistence',
    help=(
        'Choose how HAProxy should track user-to-server mappings. '
        'Stick-table persistence works with all protocols, but is broken in multi-process and multithreaded modes. '
        'Cookie-based persistence only works with HTTP/HTTPS protocols.'
    ),
    type=click.Choice(['', 'sticktable', 'cookie']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--persistence_cookiemode',
    help=(
        'Usually it is better to reuse an existing cookie. '
        'In this case HAProxy prefixes the cookie with the required information.'
    ),
    type=click.Choice(['piggyback', 'new']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--persistence_cookiename',
    help='Cookie name to use for persistence.',
    show_default=True,
    default=None
)
@click.option(
    '--persistence_stripquotes/--no-persistence_stripquotes',
    help='Enable to automatically strip quotes from the cookie value.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--stickiness_pattern',
    help='Choose a request pattern to associate a user to a server.',
    type=click.Choice(['', 'sourceipv4', 'sourceipv6', 'cookievalue', 'rdpcookie']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_dataTypes',
    help=(
            'This is used to store additional information in the stick-table. '
            'It may be used by ACLs in order to control various criteria related to the activity of the client matching '
            'the stick-table. Note that this directly impacts memory usage.'
    ),
    type=click.Choice(
        [
            '', 'conn_cnt', 'conn_cur', 'conn_rate', 'sess_cnt', 'sess_rate', 'http_req_cnt', 'http_req_rate',
            'http_err_cnt', 'http_err_rate', 'bytes_in_cnt', 'bytes_in_rate', 'bytes_out_cnt', 'bytes_out_rate'
        ]
    ),
    multiple=True,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_expire',
    help=(
        'This configures the maximum duration of an entry in the stick-table since it was last created, refreshed '
        'or matched. The maximum duration is slightly above 24 days. Enter a number followed by one of the supported '
        'suffixes "d" (days), "h" (hour), "m" (minute), "s" (seconds), "ms" (miliseconds).'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_size',
    help=(
        'This configures the maximum number of entries that can fit in the table. '
        'This value directly impacts memory usage. '
        'Count approximately 50 bytes per entry, plus the size of a string if any. '
        'Enter a number followed by one of the supported suffixes "k", "m", "g".'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_cookiename',
    help='Cookie name to use for stick table.',
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_cookielength',
    help='The maximum number of characters that will be stored in the stick table.',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--stickiness_connRatePeriod',
    help=(
        'The length of the period over which the average is measured. It reports the average incoming connection rate '
        'over that period, in connections per period. Defaults to milliseconds. '
        'Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_sessRatePeriod',
    help=(
        'The length of the period over which the average is measured. '
        'It reports the average incoming session rate over that period, '
        'in sessions per period. Defaults to milliseconds. '
        'Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_httpReqRatePeriod',
    help=(
        'The length of the period over which the average is measured. '
        'It reports the average HTTP request rate over that period, in requests per period. '
        'Defaults to milliseconds. Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_httpErrRatePeriod',
    help=(
        'The length of the period over which the average is measured. '
        'It reports the average HTTP request error rate over that period, in requests per period. '
        'Defaults to milliseconds. Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_bytesInRatePeriod',
    help=(
        'The length of the period over which the average is measured. '
        'It reports the average incoming bytes rate over that period, in bytes per period. Defaults to milliseconds. '
        'Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_bytesOutRatePeriod',
    help=(
        'The length of the period over which the average is measured. '
        'It reports the average outgoing bytes rate over that period, in bytes per period. '
        'Defaults to milliseconds. Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--basicAuthEnabled/--no-basicAuthEnabled',
    help='Enable HTTP basic authentication.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--basicAuthUsers',
    help='Basic auth users.',
    show_default=True,
    default=None
)
@click.option(
    '--basicAuthGroups',
    help='Basic auth groups.',
    show_default=True,
    default=None
)
@click.option(
    '--tuning_timeoutConnect',
    help=(
        'Set the maximum time to wait for a connection attempt to a server to succeed. '
        'Defaults to milliseconds. Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--tuning_timeoutCheck',
    help=(
        'Sets an additional read timeout for running health checks on a server. '
        'Defaults to milliseconds. Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--tuning_timeoutServer',
    help=(
        'Set the maximum inactivity time on the server side. Defaults to milliseconds. '
        'Optionally the unit may be specified as either "d", "h", "m", "s", "ms" or "us".'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--tuning_retries',
    help=(
        'Set the number of retries to perform on a server after a connection failure.'
    ),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--customOptions',
    help=(
        'These lines will be added to the HAProxy backend configuration.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--tuning_defaultserver',
    help=(
        'Default option for all server entries.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--tuning_noport/--no-tuning_noport',
    help=(
        "Don't use port on server, use the same port as frontend receive. "
        "If check enable, require port check in server."
    ),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--tuning_httpreuse',
    help=(
        'Declare how idle HTTP connections may be shared between requests.'
    ),
    type=click.Choice(['', 'never', 'safe', 'aggressive', 'always']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--tuning_caching/--no-tuning_caching',
    help=(
        'Enable caching of responses from this backend. '
        'The HAProxy cache must be enabled under Settings before this will have any effect.'
    ),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--linkedActions',
    help='Choose rules to be included in this backend pool.',
    show_default=True,
    default=None
)
@click.option(
    '--linkedErrorfiles',
    help='Choose error messages to be included in this backend pool.',
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
@pass_haproxy_backend_svc
def update(haproxy_backend_svc: HaproxyBackendFacade, **kwargs):
    """
    Update a backend.
    """
    json_payload = {
        'backend': {}
    }
    options = [
        'enabled', 'name', 'description', 'mode', 'algorithm', 'random_draws', 'proxyProtocol', 'linkedServers',
        'linkedResolver', 'resolverOpts', 'resolvePrefer', 'source', 'healthCheckEnabled', 'healthCheck',
        'healthCheckLogStatus', 'checkInterval', 'checkDownInterval', 'healthCheckFall', 'healthCheckRise',
        'linkedMailer', 'http2Enabled', 'http2Enabled_nontls', 'ba_advertised_protocols', 'persistence',
        'persistence_cookiemode', 'persistence_cookiename', 'persistence_stripquotes', 'stickiness_pattern',
        'stickiness_dataTypes', 'stickiness_expire', 'stickiness_size', 'stickiness_cookiename',
        'stickiness_cookielength', 'stickiness_connRatePeriod', 'stickiness_sessRatePeriod',
        'stickiness_httpReqRatePeriod', 'stickiness_httpErrRatePeriod', 'stickiness_bytesInRatePeriod',
        'stickiness_bytesOutRatePeriod', 'basicAuthEnabled', 'basicAuthUsers', 'basicAuthGroups',
        'tuning_timeoutConnect', 'tuning_timeoutCheck', 'tuning_timeoutServer', 'tuning_retries', 'customOptions',
        'tuning_defaultserver', 'tuning_noport', 'tuning_httpreuse', 'tuning_caching',
        'linkedActions', 'linkedErrorfiles'
    ]
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['backend'][option] = kwargs[option.lower()]

    result = haproxy_backend_svc.update_backend(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@backend.command()
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
@pass_haproxy_backend_svc
def delete(haproxy_backend_svc: HaproxyBackendFacade, **kwargs):
    """
    Delete backend
    """
    result = haproxy_backend_svc.delete_backend(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
