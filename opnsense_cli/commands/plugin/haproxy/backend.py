import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats, int_as_string
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
    Manage haproxy backend
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
    default="enabled,name,description,mode,algorithm,random_draws,proxyProtocol,linkedServers,linkedResolver,resolverOpts,resolvePrefer,source,healthCheckEnabled,healthCheck,healthCheckLogStatus,checkInterval,checkDownInterval,healthCheckFall,healthCheckRise,linkedMailer,http2Enabled,http2Enabled_nontls,ba_advertised_protocols,persistence,persistence_cookiemode,persistence_cookiename,persistence_stripquotes,stickiness_pattern,stickiness_dataTypes,stickiness_expire,stickiness_size,stickiness_cookiename,stickiness_cookielength,stickiness_connRatePeriod,stickiness_sessRatePeriod,stickiness_httpReqRatePeriod,stickiness_httpErrRatePeriod,stickiness_bytesInRatePeriod,stickiness_bytesOutRatePeriod,basicAuthEnabled,basicAuthUsers,basicAuthGroups,tuning_timeoutConnect,tuning_timeoutCheck,tuning_timeoutServer,tuning_retries,customOptions,tuning_defaultserver,tuning_noport,tuning_httpreuse,tuning_caching,linkedActions,linkedErrorfiles"
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
    default="enabled,id,name,type,address,port,description",
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
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--description',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--mode',
    help='ToDo',
    type=click.Choice(['http', 'tcp']),
    multiple=False,
    show_default=True,
    default='http',
    required=True,
)
@click.option(
    '--algorithm',
    help='ToDo',
    type=click.Choice(['source', 'roundrobin', 'static-rr', 'leastconn', 'uri', 'random']),
    multiple=False,
    show_default=True,
    default='source',
    required=True,
)
@click.option(
    '--random_draws',
    help='ToDo',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=2,
    required=True,
)
@click.option(
    '--proxyProtocol',
    help='ToDo',
    type=click.Choice(['', 'v1', 'v2']),
    multiple=False,
    show_default=True,
    default='None',
    required=False,
)
@click.option(
    '--linkedServers',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--linkedResolver',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--resolverOpts',
    help='ToDo',
    type=click.Choice(['', 'allow-dup-ip', 'ignore-weight', 'prevent-dup-ip']),
    multiple=True,
    show_default=True,
    default=[],
    required=False,
)
@click.option(
    '--resolvePrefer',
    help='ToDo',
    type=click.Choice(['', 'ipv4', 'ipv6']),
    multiple=False,
    show_default=True,
    default='None',
    required=False,
)
@click.option(
    '--source',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--healthCheckEnabled/--no-healthCheckEnabled',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--healthCheck',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--healthCheckLogStatus/--no-healthCheckLogStatus',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--checkInterval',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--checkDownInterval',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--healthCheckFall',
    help='ToDo',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--healthCheckRise',
    help='ToDo',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--linkedMailer',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http2Enabled/--no-http2Enabled',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--http2Enabled_nontls/--no-http2Enabled_nontls',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--ba_advertised_protocols',
    help='ToDo',
    type=click.Choice(['', 'h2', 'http11', 'http10']),
    multiple=True,
    show_default=True,
    default=['h2', 'http11'],
    required=False,
)
@click.option(
    '--persistence',
    help='ToDo',
    type=click.Choice(['', 'sticktable', 'cookie']),
    multiple=False,
    show_default=True,
    default='sticktable',
    required=False,
)
@click.option(
    '--persistence_cookiemode',
    help='ToDo',
    type=click.Choice(['piggyback', 'new']),
    multiple=False,
    show_default=True,
    default='piggyback',
    required=True,
)
@click.option(
    '--persistence_cookiename',
    help='ToDo',
    show_default=True,
    default='SRVCOOKIE',
    required=False,
)
@click.option(
    '--persistence_stripquotes/--no-persistence_stripquotes',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--stickiness_pattern',
    help='ToDo',
    type=click.Choice(['', 'sourceipv4', 'sourceipv6', 'cookievalue', 'rdpcookie']),
    multiple=False,
    show_default=True,
    default='sourceipv4',
    required=False,
)
@click.option(
    '--stickiness_dataTypes',
    help='ToDo',
    type=click.Choice(['', 'conn_cnt', 'conn_cur', 'conn_rate', 'sess_cnt', 'sess_rate', 'http_req_cnt', 'http_req_rate', 'http_err_cnt', 'http_err_rate', 'bytes_in_cnt', 'bytes_in_rate', 'bytes_out_cnt', 'bytes_out_rate']),
    multiple=True,
    show_default=True,
    default=[],
    required=False,
)
@click.option(
    '--stickiness_expire',
    help='ToDo',
    show_default=True,
    default='30m',
    required=True,
)
@click.option(
    '--stickiness_size',
    help='ToDo',
    show_default=True,
    default='50k',
    required=True,
)
@click.option(
    '--stickiness_cookiename',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--stickiness_cookielength',
    help='ToDo',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--stickiness_connRatePeriod',
    help='ToDo',
    show_default=True,
    default='10s',
    required=False,
)
@click.option(
    '--stickiness_sessRatePeriod',
    help='ToDo',
    show_default=True,
    default='10s',
    required=False,
)
@click.option(
    '--stickiness_httpReqRatePeriod',
    help='ToDo',
    show_default=True,
    default='10s',
    required=False,
)
@click.option(
    '--stickiness_httpErrRatePeriod',
    help='ToDo',
    show_default=True,
    default='10s',
    required=False,
)
@click.option(
    '--stickiness_bytesInRatePeriod',
    help='ToDo',
    show_default=True,
    default='1m',
    required=False,
)
@click.option(
    '--stickiness_bytesOutRatePeriod',
    help='ToDo',
    show_default=True,
    default='1m',
    required=False,
)
@click.option(
    '--basicAuthEnabled/--no-basicAuthEnabled',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--basicAuthUsers',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--basicAuthGroups',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tuning_timeoutConnect',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tuning_timeoutCheck',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tuning_timeoutServer',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tuning_retries',
    help='ToDo',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--customOptions',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tuning_defaultserver',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tuning_noport/--no-tuning_noport',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--tuning_httpreuse',
    help='ToDo',
    type=click.Choice(['', 'never', 'safe', 'aggressive', 'always']),
    multiple=False,
    show_default=True,
    default='safe',
    required=False,
)
@click.option(
    '--tuning_caching/--no-tuning_caching',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--linkedActions',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--linkedErrorfiles',
    help='ToDo',
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
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--name',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--description',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--mode',
    help='ToDo',
    type=click.Choice(['http', 'tcp']),
    multiple=False,
    show_default=True,
    default=None
)
@click.option(
    '--algorithm',
    help='ToDo',
    type=click.Choice(['source', 'roundrobin', 'static-rr', 'leastconn', 'uri', 'random']),
    multiple=False,
    show_default=True,
    default=None
)
@click.option(
    '--random_draws',
    help='ToDo',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--proxyProtocol',
    help='ToDo',
    type=click.Choice(['', 'v1', 'v2']),
    multiple=False,
    show_default=True,
    default=None
)
@click.option(
    '--linkedServers',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--linkedResolver',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--resolverOpts',
    help='ToDo',
    type=click.Choice(['', 'allow-dup-ip', 'ignore-weight', 'prevent-dup-ip']),
    multiple=True,
    show_default=True,
    default=None
)
@click.option(
    '--resolvePrefer',
    help='ToDo',
    type=click.Choice(['', 'ipv4', 'ipv6']),
    multiple=False,
    show_default=True,
    default=None
)
@click.option(
    '--source',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--healthCheckEnabled/--no-healthCheckEnabled',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--healthCheck',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--healthCheckLogStatus/--no-healthCheckLogStatus',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--checkInterval',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--checkDownInterval',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--healthCheckFall',
    help='ToDo',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--healthCheckRise',
    help='ToDo',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--linkedMailer',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--http2Enabled/--no-http2Enabled',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--http2Enabled_nontls/--no-http2Enabled_nontls',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--ba_advertised_protocols',
    help='ToDo',
    type=click.Choice(['', 'h2', 'http11', 'http10']),
    multiple=True,
    show_default=True,
    default=None
)
@click.option(
    '--persistence',
    help='ToDo',
    type=click.Choice(['', 'sticktable', 'cookie']),
    multiple=False,
    show_default=True,
    default=None
)
@click.option(
    '--persistence_cookiemode',
    help='ToDo',
    type=click.Choice(['piggyback', 'new']),
    multiple=False,
    show_default=True,
    default=None
)
@click.option(
    '--persistence_cookiename',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--persistence_stripquotes/--no-persistence_stripquotes',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--stickiness_pattern',
    help='ToDo',
    type=click.Choice(['', 'sourceipv4', 'sourceipv6', 'cookievalue', 'rdpcookie']),
    multiple=False,
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_dataTypes',
    help='ToDo',
    type=click.Choice(['', 'conn_cnt', 'conn_cur', 'conn_rate', 'sess_cnt', 'sess_rate', 'http_req_cnt', 'http_req_rate', 'http_err_cnt', 'http_err_rate', 'bytes_in_cnt', 'bytes_in_rate', 'bytes_out_cnt', 'bytes_out_rate']),
    multiple=True,
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_expire',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_size',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_cookiename',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_cookielength',
    help='ToDo',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--stickiness_connRatePeriod',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_sessRatePeriod',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_httpReqRatePeriod',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_httpErrRatePeriod',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_bytesInRatePeriod',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_bytesOutRatePeriod',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--basicAuthEnabled/--no-basicAuthEnabled',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--basicAuthUsers',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--basicAuthGroups',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--tuning_timeoutConnect',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--tuning_timeoutCheck',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--tuning_timeoutServer',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--tuning_retries',
    help='ToDo',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--customOptions',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--tuning_defaultserver',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--tuning_noport/--no-tuning_noport',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--tuning_httpreuse',
    help='ToDo',
    type=click.Choice(['', 'never', 'safe', 'aggressive', 'always']),
    multiple=False,
    show_default=True,
    default=None
)
@click.option(
    '--tuning_caching/--no-tuning_caching',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--linkedActions',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--linkedErrorfiles',
    help='ToDo',
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
    options = ['enabled', 'name', 'description', 'mode', 'algorithm', 'random_draws', 'proxyProtocol', 'linkedServers', 'linkedResolver', 'resolverOpts', 'resolvePrefer', 'source', 'healthCheckEnabled', 'healthCheck', 'healthCheckLogStatus', 'checkInterval', 'checkDownInterval', 'healthCheckFall', 'healthCheckRise', 'linkedMailer', 'http2Enabled', 'http2Enabled_nontls', 'ba_advertised_protocols', 'persistence', 'persistence_cookiemode', 'persistence_cookiename', 'persistence_stripquotes', 'stickiness_pattern', 'stickiness_dataTypes', 'stickiness_expire', 'stickiness_size', 'stickiness_cookiename', 'stickiness_cookielength', 'stickiness_connRatePeriod', 'stickiness_sessRatePeriod', 'stickiness_httpReqRatePeriod', 'stickiness_httpErrRatePeriod', 'stickiness_bytesInRatePeriod', 'stickiness_bytesOutRatePeriod', 'basicAuthEnabled', 'basicAuthUsers', 'basicAuthGroups', 'tuning_timeoutConnect', 'tuning_timeoutCheck', 'tuning_timeoutServer', 'tuning_retries', 'customOptions', 'tuning_defaultserver', 'tuning_noport', 'tuning_httpreuse', 'tuning_caching', 'linkedActions', 'linkedErrorfiles']
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
