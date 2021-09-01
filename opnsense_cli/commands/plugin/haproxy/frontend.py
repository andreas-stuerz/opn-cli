import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats, int_as_string, tuple_to_csv
from opnsense_cli.commands.plugin.haproxy import haproxy
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.haproxy import Settings, Service
from opnsense_cli.facades.commands.plugin.haproxy.frontend import HaproxyFrontendFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_haproxy_frontend_svc = click.make_pass_decorator(HaproxyFrontendFacade)


@haproxy.group()
@pass_api_client
@click.pass_context
def frontend(ctx, api_client: ApiClient, **kwargs):
    """
    Manage haproxy frontend
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
        "uuid,enabled,name,description,bind,bindOptions,mode,Backend,"
        "ssl_enabled,ssl_certificates,ssl_default_certificate"
    ),
    show_default=True,
)
@pass_haproxy_frontend_svc
def list(haproxy_frontend_svc: HaproxyFrontendFacade, **kwargs):
    """
    Show all frontend
    """
    result = haproxy_frontend_svc.list_frontends()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@frontend.command()
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
        "enabled,name,description,bind,bindOptions,mode,Backend,defaultBackend,ssl_enabled,ssl_certificates,"
        "ssl_default_certificate,ssl_customOptions,ssl_advancedEnabled,ssl_bindOptions,ssl_minVersion,ssl_maxVersion,"
        "ssl_cipherList,ssl_cipherSuites,ssl_hstsEnabled,ssl_hstsIncludeSubDomains,ssl_hstsPreload,ssl_hstsMaxAge,"
        "ssl_clientAuthEnabled,ssl_clientAuthVerify,ssl_clientAuthCAs,ssl_clientAuthCRLs,basicAuthEnabled,"
        "Users,basicAuthUsers,Groups,basicAuthGroups,tuning_maxConnections,tuning_timeoutClient,tuning_timeoutHttpReq,"
        "tuning_timeoutHttpKeepAlive,Cpus,linkedCpuAffinityRules,logging_dontLogNull,logging_dontLogNormal,"
        "logging_logSeparateErrors,logging_detailedLog,logging_socketStats,stickiness_pattern,stickiness_dataTypes,"
        "stickiness_expire,stickiness_size,stickiness_counter,stickiness_counter_key,stickiness_length,"
        "stickiness_connRatePeriod,stickiness_sessRatePeriod,stickiness_httpReqRatePeriod,stickiness_httpErrRatePeriod,"
        "stickiness_bytesInRatePeriod,stickiness_bytesOutRatePeriod,http2Enabled,http2Enabled_nontls,"
        "advertised_protocols,forwardFor,connectionBehaviour,customOptions,Actions,"
        "linkedActions,Errorfiles,linkedErrorfiles"
    ),
    show_default=True,
)
@pass_haproxy_frontend_svc
def show(haproxy_frontend_svc: HaproxyFrontendFacade, **kwargs):
    """
    Show details for frontend
    """
    result = haproxy_frontend_svc.show_frontend(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@frontend.command()
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
    '--bind',
    help='ToDo',
    show_default=True,
    default=None,
    required=True,
)
@click.option(
    '--bindOptions',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--mode',
    help='ToDo',
    type=click.Choice(['http', 'ssl', 'tcp']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='http',
    required=True,
)
@click.option(
    '--defaultBackend',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--ssl_enabled/--no-ssl_enabled',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--ssl_certificates',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--ssl_default_certificate',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--ssl_customOptions',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--ssl_advancedEnabled/--no-ssl_advancedEnabled',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--ssl_bindOptions',
    help='ToDo',
    type=click.Choice(['', 'no-sslv3', 'no-tlsv10', 'no-tlsv11', 'no-tlsv12', 'no-tlsv13', 'no-tls-tickets', 'force-sslv3', 'force-tlsv10', 'force-tlsv11', 'force-tlsv12', 'force-tlsv13', 'prefer-client-ciphers', 'strict-sni']),
    multiple=True,
    callback=tuple_to_csv,
    show_default=True,
    default=['prefer-client-ciphers'],
    required=False,
)
@click.option(
    '--ssl_minVersion',
    help='ToDo',
    type=click.Choice(['', 'SSLv3', 'TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='TLSv1.2',
    required=False,
)
@click.option(
    '--ssl_maxVersion',
    help='ToDo',
    type=click.Choice(['', 'SSLv3', 'TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--ssl_cipherList',
    help='ToDo',
    show_default=True,
    default='ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256',
    required=False,
)
@click.option(
    '--ssl_cipherSuites',
    help='ToDo',
    show_default=True,
    default='TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256',
    required=False,
)
@click.option(
    '--ssl_hstsEnabled/--no-ssl_hstsEnabled',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--ssl_hstsIncludeSubDomains/--no-ssl_hstsIncludeSubDomains',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--ssl_hstsPreload/--no-ssl_hstsPreload',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--ssl_hstsMaxAge',
    help='ToDo',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=15768000,
    required=True,
)
@click.option(
    '--ssl_clientAuthEnabled/--no-ssl_clientAuthEnabled',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--ssl_clientAuthVerify',
    help='ToDo',
    type=click.Choice(['', 'none', 'optional', 'required']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='required',
    required=False,
)
@click.option(
    '--ssl_clientAuthCAs',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--ssl_clientAuthCRLs',
    help='ToDo',
    show_default=True,
    default=None,
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
    '--tuning_maxConnections',
    help='ToDo',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--tuning_timeoutClient',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tuning_timeoutHttpReq',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tuning_timeoutHttpKeepAlive',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--linkedCpuAffinityRules',
    help='ToDo',
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--logging_dontLogNull/--no-logging_dontLogNull',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--logging_dontLogNormal/--no-logging_dontLogNormal',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--logging_logSeparateErrors/--no-logging_logSeparateErrors',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--logging_detailedLog/--no-logging_detailedLog',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--logging_socketStats/--no-logging_socketStats',
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
    type=click.Choice(['', 'ipv4', 'ipv6', 'integer', 'string', 'binary']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--stickiness_dataTypes',
    help='ToDo',
    type=click.Choice(['', 'conn_cnt', 'conn_cur', 'conn_rate', 'sess_cnt', 'sess_rate', 'http_req_cnt', 'http_req_rate', 'http_err_cnt', 'http_err_rate', 'bytes_in_cnt', 'bytes_in_rate', 'bytes_out_cnt', 'bytes_out_rate']),
    multiple=True,
    callback=tuple_to_csv,
    show_default=True,
    default=None,
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
    '--stickiness_counter/--no-stickiness_counter',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--stickiness_counter_key',
    help='ToDo',
    show_default=True,
    default='src',
    required=False,
)
@click.option(
    '--stickiness_length',
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
    '--advertised_protocols',
    help='ToDo',
    type=click.Choice(['', 'h2', 'http11', 'http10']),
    multiple=True,
    callback=tuple_to_csv,
    show_default=True,
    default=['h2', 'http11'],
    required=False,
)
@click.option(
    '--forwardFor/--no-forwardFor',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--connectionBehaviour',
    help='ToDo',
    type=click.Choice(['http-keep-alive', 'http-tunnel', 'httpclose', 'http-server-close', 'forceclose']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='http-keep-alive',
    required=True,
)
@click.option(
    '--customOptions',
    help='ToDo',
    show_default=True,
    default=None,
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
@pass_haproxy_frontend_svc
def create(haproxy_frontend_svc: HaproxyFrontendFacade, **kwargs):
    """
    Create a new frontend
    """
    json_payload = {
        'frontend': {
            "enabled": kwargs['enabled'],
            "name": kwargs['name'],
            "description": kwargs['description'],
            "bind": kwargs['bind'],
            "bindOptions": kwargs['bindoptions'],
            "mode": kwargs['mode'],
            "defaultBackend": kwargs['defaultbackend'],
            "ssl_enabled": kwargs['ssl_enabled'],
            "ssl_certificates": kwargs['ssl_certificates'],
            "ssl_default_certificate": kwargs['ssl_default_certificate'],
            "ssl_customOptions": kwargs['ssl_customoptions'],
            "ssl_advancedEnabled": kwargs['ssl_advancedenabled'],
            "ssl_bindOptions": kwargs['ssl_bindoptions'],
            "ssl_minVersion": kwargs['ssl_minversion'],
            "ssl_maxVersion": kwargs['ssl_maxversion'],
            "ssl_cipherList": kwargs['ssl_cipherlist'],
            "ssl_cipherSuites": kwargs['ssl_ciphersuites'],
            "ssl_hstsEnabled": kwargs['ssl_hstsenabled'],
            "ssl_hstsIncludeSubDomains": kwargs['ssl_hstsincludesubdomains'],
            "ssl_hstsPreload": kwargs['ssl_hstspreload'],
            "ssl_hstsMaxAge": kwargs['ssl_hstsmaxage'],
            "ssl_clientAuthEnabled": kwargs['ssl_clientauthenabled'],
            "ssl_clientAuthVerify": kwargs['ssl_clientauthverify'],
            "ssl_clientAuthCAs": kwargs['ssl_clientauthcas'],
            "ssl_clientAuthCRLs": kwargs['ssl_clientauthcrls'],
            "basicAuthEnabled": kwargs['basicauthenabled'],
            "basicAuthUsers": kwargs['basicauthusers'],
            "basicAuthGroups": kwargs['basicauthgroups'],
            "tuning_maxConnections": kwargs['tuning_maxconnections'],
            "tuning_timeoutClient": kwargs['tuning_timeoutclient'],
            "tuning_timeoutHttpReq": kwargs['tuning_timeouthttpreq'],
            "tuning_timeoutHttpKeepAlive": kwargs['tuning_timeouthttpkeepalive'],
            "linkedCpuAffinityRules": kwargs['linkedcpuaffinityrules'],
            "logging_dontLogNull": kwargs['logging_dontlognull'],
            "logging_dontLogNormal": kwargs['logging_dontlognormal'],
            "logging_logSeparateErrors": kwargs['logging_logseparateerrors'],
            "logging_detailedLog": kwargs['logging_detailedlog'],
            "logging_socketStats": kwargs['logging_socketstats'],
            "stickiness_pattern": kwargs['stickiness_pattern'],
            "stickiness_dataTypes": kwargs['stickiness_datatypes'],
            "stickiness_expire": kwargs['stickiness_expire'],
            "stickiness_size": kwargs['stickiness_size'],
            "stickiness_counter": kwargs['stickiness_counter'],
            "stickiness_counter_key": kwargs['stickiness_counter_key'],
            "stickiness_length": kwargs['stickiness_length'],
            "stickiness_connRatePeriod": kwargs['stickiness_connrateperiod'],
            "stickiness_sessRatePeriod": kwargs['stickiness_sessrateperiod'],
            "stickiness_httpReqRatePeriod": kwargs['stickiness_httpreqrateperiod'],
            "stickiness_httpErrRatePeriod": kwargs['stickiness_httperrrateperiod'],
            "stickiness_bytesInRatePeriod": kwargs['stickiness_bytesinrateperiod'],
            "stickiness_bytesOutRatePeriod": kwargs['stickiness_bytesoutrateperiod'],
            "http2Enabled": kwargs['http2enabled'],
            "http2Enabled_nontls": kwargs['http2enabled_nontls'],
            "advertised_protocols": kwargs['advertised_protocols'],
            "forwardFor": kwargs['forwardfor'],
            "connectionBehaviour": kwargs['connectionbehaviour'],
            "customOptions": kwargs['customoptions'],
            "linkedActions": kwargs['linkedactions'],
            "linkedErrorfiles": kwargs['linkederrorfiles'],
            
        }
    }

    result = haproxy_frontend_svc.create_frontend(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@frontend.command()
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
    '--bind',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--bindOptions',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--mode',
    help='ToDo',
    type=click.Choice(['http', 'ssl', 'tcp']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--defaultBackend',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--ssl_enabled/--no-ssl_enabled',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--ssl_certificates',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--ssl_default_certificate',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--ssl_customOptions',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--ssl_advancedEnabled/--no-ssl_advancedEnabled',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--ssl_bindOptions',
    help='ToDo',
    type=click.Choice(['', 'no-sslv3', 'no-tlsv10', 'no-tlsv11', 'no-tlsv12', 'no-tlsv13', 'no-tls-tickets', 'force-sslv3', 'force-tlsv10', 'force-tlsv11', 'force-tlsv12', 'force-tlsv13', 'prefer-client-ciphers', 'strict-sni']),
    multiple=True,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--ssl_minVersion',
    help='ToDo',
    type=click.Choice(['', 'SSLv3', 'TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--ssl_maxVersion',
    help='ToDo',
    type=click.Choice(['', 'SSLv3', 'TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--ssl_cipherList',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--ssl_cipherSuites',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--ssl_hstsEnabled/--no-ssl_hstsEnabled',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--ssl_hstsIncludeSubDomains/--no-ssl_hstsIncludeSubDomains',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--ssl_hstsPreload/--no-ssl_hstsPreload',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--ssl_hstsMaxAge',
    help='ToDo',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--ssl_clientAuthEnabled/--no-ssl_clientAuthEnabled',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--ssl_clientAuthVerify',
    help='ToDo',
    type=click.Choice(['', 'none', 'optional', 'required']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--ssl_clientAuthCAs',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--ssl_clientAuthCRLs',
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
    '--tuning_maxConnections',
    help='ToDo',
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--tuning_timeoutClient',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--tuning_timeoutHttpReq',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--tuning_timeoutHttpKeepAlive',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--linkedCpuAffinityRules',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--logging_dontLogNull/--no-logging_dontLogNull',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--logging_dontLogNormal/--no-logging_dontLogNormal',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--logging_logSeparateErrors/--no-logging_logSeparateErrors',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--logging_detailedLog/--no-logging_detailedLog',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--logging_socketStats/--no-logging_socketStats',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--stickiness_pattern',
    help='ToDo',
    type=click.Choice(['', 'ipv4', 'ipv6', 'integer', 'string', 'binary']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_dataTypes',
    help='ToDo',
    type=click.Choice(['', 'conn_cnt', 'conn_cur', 'conn_rate', 'sess_cnt', 'sess_rate', 'http_req_cnt', 'http_req_rate', 'http_err_cnt', 'http_err_rate', 'bytes_in_cnt', 'bytes_in_rate', 'bytes_out_cnt', 'bytes_out_rate']),
    multiple=True,
    callback=tuple_to_csv,
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
    '--stickiness_counter/--no-stickiness_counter',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--stickiness_counter_key',
    help='ToDo',
    show_default=True,
    default=None
)
@click.option(
    '--stickiness_length',
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
    '--advertised_protocols',
    help='ToDo',
    type=click.Choice(['', 'h2', 'http11', 'http10']),
    multiple=True,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--forwardFor/--no-forwardFor',
    help='ToDo',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--connectionBehaviour',
    help='ToDo',
    type=click.Choice(['http-keep-alive', 'http-tunnel', 'httpclose', 'http-server-close', 'forceclose']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--customOptions',
    help='ToDo',
    show_default=True,
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
@pass_haproxy_frontend_svc
def update(haproxy_frontend_svc: HaproxyFrontendFacade, **kwargs):
    """
    Update a frontend.
    """
    json_payload = {
        'frontend': {}
    }
    options = ['enabled', 'name', 'description', 'bind', 'bindOptions', 'mode', 'defaultBackend', 'ssl_enabled', 'ssl_certificates', 'ssl_default_certificate', 'ssl_customOptions', 'ssl_advancedEnabled', 'ssl_bindOptions', 'ssl_minVersion', 'ssl_maxVersion', 'ssl_cipherList', 'ssl_cipherSuites', 'ssl_hstsEnabled', 'ssl_hstsIncludeSubDomains', 'ssl_hstsPreload', 'ssl_hstsMaxAge', 'ssl_clientAuthEnabled', 'ssl_clientAuthVerify', 'ssl_clientAuthCAs', 'ssl_clientAuthCRLs', 'basicAuthEnabled', 'basicAuthUsers', 'basicAuthGroups', 'tuning_maxConnections', 'tuning_timeoutClient', 'tuning_timeoutHttpReq', 'tuning_timeoutHttpKeepAlive', 'linkedCpuAffinityRules', 'logging_dontLogNull', 'logging_dontLogNormal', 'logging_logSeparateErrors', 'logging_detailedLog', 'logging_socketStats', 'stickiness_pattern', 'stickiness_dataTypes', 'stickiness_expire', 'stickiness_size', 'stickiness_counter', 'stickiness_counter_key', 'stickiness_length', 'stickiness_connRatePeriod', 'stickiness_sessRatePeriod', 'stickiness_httpReqRatePeriod', 'stickiness_httpErrRatePeriod', 'stickiness_bytesInRatePeriod', 'stickiness_bytesOutRatePeriod', 'http2Enabled', 'http2Enabled_nontls', 'advertised_protocols', 'forwardFor', 'connectionBehaviour', 'customOptions', 'linkedActions', 'linkedErrorfiles']
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['frontend'][option] = kwargs[option.lower()]

    result = haproxy_frontend_svc.update_frontend(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@frontend.command()
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
@pass_haproxy_frontend_svc
def delete(haproxy_frontend_svc: HaproxyFrontendFacade, **kwargs):
    """
    Delete frontend
    """
    result = haproxy_frontend_svc.delete_frontend(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
