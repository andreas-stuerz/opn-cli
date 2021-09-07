import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats, int_as_string, tuple_to_csv
from opnsense_cli.commands.plugin.haproxy import haproxy
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.haproxy import Settings, Service
from opnsense_cli.facades.commands.plugin.haproxy.healthcheck import HaproxyHealthcheckFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_haproxy_healthcheck_svc = click.make_pass_decorator(HaproxyHealthcheckFacade)


@haproxy.group()
@pass_api_client
@click.pass_context
def healthcheck(ctx, api_client: ApiClient, **kwargs):
    """
    Determine if a server is able to respond to client request.
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = HaproxyHealthcheckFacade(settings_api, service_api)


@healthcheck.command()
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
        "uuid,name,description,type,interval"
    ),
    show_default=True,
)
@pass_haproxy_healthcheck_svc
def list(haproxy_healthcheck_svc: HaproxyHealthcheckFacade, **kwargs):
    """
    Show all healthcheck
    """
    result = haproxy_healthcheck_svc.list_healthchecks()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@healthcheck.command()
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
        "name,description,type,interval,force_ssl,checkport,http_method,http_uri,http_version,http_host,"
        "http_expressionEnabled,http_expression,http_negate,http_value,tcp_enabled,tcp_sendValue,"
        "tcp_matchType,tcp_negate,tcp_matchValue,agent_port,mysql_user,mysql_post41,pgsql_user,"
        "smtp_domain,esmtp_domain,agentPort,dbUser,smtpDomain"
    ),
    show_default=True,
)
@pass_haproxy_healthcheck_svc
def show(haproxy_healthcheck_svc: HaproxyHealthcheckFacade, **kwargs):
    """
    Show details for healthcheck
    """
    result = haproxy_healthcheck_svc.show_healthcheck(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@healthcheck.command()
@click.argument('name')
@click.option(
    '--description',
    help=('Description for this Health Monitor.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--type',
    help=('Select type of health check.'),
    type=click.Choice(['tcp', 'http', 'agent', 'ldap', 'mysql', 'pgsql', 'redis', 'smtp', 'esmtp', 'ssl']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='http',
    required=True,
)
@click.option(
    '--interval',
    help=(
        'Select interval (in milliseconds) between two consecutive health checks. '
        'This value can be overriden in backend pool and real server configuration.'
    ),
    show_default=True,
    default='2s',
    required=True,
)
@click.option(
    '--force_ssl/--no-force_ssl',
    help=(
        'This option forces encryption of all health checks over SSL, '
        'regardless of whether the server uses SSL or not for the normal traffic.'
    ),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--checkport',
    help=('Provide the TCP communication port to use during check, i.e. 80 or 443.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--http_method',
    help=('Select HTTP method for health check.'),
    type=click.Choice(['', 'options', 'head', 'get', 'put', 'post', 'delete', 'trace']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='options',
    required=False,
)
@click.option(
    '--http_uri',
    help=('Specify HTTP request URI for health check.'),
    show_default=True,
    default='/',
    required=False,
)
@click.option(
    '--http_version',
    help=('Select HTTP version for a HTTP health check.'),
    type=click.Choice(['', 'http10', 'http11', 'http2']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='http10',
    required=False,
)
@click.option(
    '--http_host',
    help=('Specify HTTP host to use for health check. Requires HTTP/1.1.'),
    show_default=True,
    default='localhost',
    required=False,
)
@click.option(
    '--http_expressionEnabled/--no-http_expressionEnabled',
    help=('None'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--http_expression',
    help=('Select health check expression.'),
    type=click.Choice(['', 'status', 'rstatus', 'string', 'rstring']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_negate/--no-http_negate',
    help=('Use this to invert the meaning of the expression.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--http_value',
    help=(
        'Specify a value to match with the expression. '
        'NOTE: It is important to note that the responses will be limited to a certain size defined by '
        'the global "tune.chksize" option, which defaults to 16384 bytes.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tcp_enabled/--no-tcp_enabled',
    help=('Enable tcp check'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--tcp_sendValue',
    help=(
        'Specify a value to match with the expression. NOTE: It is important to note that the responses will be '
        'limited to a certain size defined by the global "tune.chksize" option, which defaults to 16384 bytes.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tcp_matchType',
    help=('Select how to look for a specific pattern in the response.'),
    type=click.Choice(['', 'string', 'rstring', 'binary']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='string',
    required=False,
)
@click.option(
    '--tcp_negate/--no-tcp_negate',
    help=('Use this to invert the meaning of the expression.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--tcp_matchValue',
    help=(
        'Specify the pattern to look for in the response buffer. If the match is set to binary, '
        'then the pattern must be passed as a serie of hexadecimal digits in an even number.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--agent_port',
    help=('Specify the TCP port used for agent checks.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--mysql_user',
    help=('Specify the username to be used for database health checks.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--mysql_post41/--no-mysql_post41',
    help=('Send checks compatible with MySQL server 4.1 and later.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=False,
)
@click.option(
    '--pgsql_user',
    help=('Specify the username to be used for database health checks.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--smtp_domain',
    help=('Specify the domain name to present to the server for SMTP health checks.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--esmtp_domain',
    help=('Specify the domain name to present to the server for ESMTP health checks.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--agentPort',
    help=('Enable agent checks'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--dbUser',
    help=('MySQL database user'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--smtpDomain',
    help=('None'),
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
@pass_haproxy_healthcheck_svc
def create(haproxy_healthcheck_svc: HaproxyHealthcheckFacade, **kwargs):
    """
    Create a new healthcheck
    """
    json_payload = {
        'healthcheck': {
            "name": kwargs['name'],
            "description": kwargs['description'],
            "type": kwargs['type'],
            "interval": kwargs['interval'],
            "force_ssl": kwargs['force_ssl'],
            "checkport": kwargs['checkport'],
            "http_method": kwargs['http_method'],
            "http_uri": kwargs['http_uri'],
            "http_version": kwargs['http_version'],
            "http_host": kwargs['http_host'],
            "http_expressionEnabled": kwargs['http_expressionenabled'],
            "http_expression": kwargs['http_expression'],
            "http_negate": kwargs['http_negate'],
            "http_value": kwargs['http_value'],
            "tcp_enabled": kwargs['tcp_enabled'],
            "tcp_sendValue": kwargs['tcp_sendvalue'],
            "tcp_matchType": kwargs['tcp_matchtype'],
            "tcp_negate": kwargs['tcp_negate'],
            "tcp_matchValue": kwargs['tcp_matchvalue'],
            "agent_port": kwargs['agent_port'],
            "mysql_user": kwargs['mysql_user'],
            "mysql_post41": kwargs['mysql_post41'],
            "pgsql_user": kwargs['pgsql_user'],
            "smtp_domain": kwargs['smtp_domain'],
            "esmtp_domain": kwargs['esmtp_domain'],
            "agentPort": kwargs['agentport'],
            "dbUser": kwargs['dbuser'],
            "smtpDomain": kwargs['smtpdomain'],
        }
    }

    result = haproxy_healthcheck_svc.create_healthcheck(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@healthcheck.command()
@click.argument('uuid')
@click.option(
    '--name',
    help=('Name to identify this Health Monitor.'),
    show_default=True,
    default=None
)
@click.option(
    '--description',
    help=('Description for this Health Monitor.'),
    show_default=True,
    default=None
)
@click.option(
    '--type',
    help=('Select type of health check.'),
    type=click.Choice(['tcp', 'http', 'agent', 'ldap', 'mysql', 'pgsql', 'redis', 'smtp', 'esmtp', 'ssl']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--interval',
    help=(
        'Select interval (in milliseconds) between two consecutive health checks. '
        'This value can be overriden in backend pool and real server configuration.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--force_ssl/--no-force_ssl',
    help=(
        'This option forces encryption of all health checks over SSL, '
        'regardless of whether the server uses SSL or not for the normal traffic.'
    ),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--checkport',
    help=('Provide the TCP communication port to use during check, i.e. 80 or 443.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--http_method',
    help=('Select HTTP method for health check.'),
    type=click.Choice(['', 'options', 'head', 'get', 'put', 'post', 'delete', 'trace']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--http_uri',
    help=('Specify HTTP request URI for health check.'),
    show_default=True,
    default=None
)
@click.option(
    '--http_version',
    help=('Select HTTP version for a HTTP health check.'),
    type=click.Choice(['', 'http10', 'http11', 'http2']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--http_host',
    help=('Specify HTTP host to use for health check. Requires HTTP/1.1.'),
    show_default=True,
    default=None
)
@click.option(
    '--http_expressionEnabled/--no-http_expressionEnabled',
    help=('None'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--http_expression',
    help=('Select health check expression.'),
    type=click.Choice(['', 'status', 'rstatus', 'string', 'rstring']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--http_negate/--no-http_negate',
    help=('Use this to invert the meaning of the expression.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--http_value',
    help=(
        'Specify a value to match with the expression. NOTE: It is important to note that the responses will be '
        'limited to a certain size defined by the global "tune.chksize" option, which defaults to 16384 bytes.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--tcp_enabled/--no-tcp_enabled',
    help=('Enable tcp check'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--tcp_sendValue',
    help=(
        'Specify a value to match with the expression. NOTE: It is important to note that the responses will be '
        'limited to a certain size defined by the global "tune.chksize" option, which defaults to 16384 bytes.'),
    show_default=True,
    default=None
)
@click.option(
    '--tcp_matchType',
    help=('Select how to look for a specific pattern in the response.'),
    type=click.Choice(['', 'string', 'rstring', 'binary']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--tcp_negate/--no-tcp_negate',
    help=('Use this to invert the meaning of the expression.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--tcp_matchValue',
    help=(
        'Specify the pattern to look for in the response buffer. If the match is set to binary, '
        'then the pattern must be passed as a serie of hexadecimal digits in an even number.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--agent_port',
    help=('Specify the TCP port used for agent checks.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--mysql_user',
    help=('Specify the username to be used for database health checks.'),
    show_default=True,
    default=None
)
@click.option(
    '--mysql_post41/--no-mysql_post41',
    help=('Send checks compatible with MySQL server 4.1 and later.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--pgsql_user',
    help=('Specify the username to be used for database health checks.'),
    show_default=True,
    default=None
)
@click.option(
    '--smtp_domain',
    help=('Specify the domain name to present to the server for SMTP health checks.'),
    show_default=True,
    default=None
)
@click.option(
    '--esmtp_domain',
    help=('Specify the domain name to present to the server for ESMTP health checks.'),
    show_default=True,
    default=None
)
@click.option(
    '--agentPort',
    help=('Agent check port'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--dbUser',
    help=('MySQL database user'),
    show_default=True,
    default=None
)
@click.option(
    '--smtpDomain',
    help=('None'),
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
@pass_haproxy_healthcheck_svc
def update(haproxy_healthcheck_svc: HaproxyHealthcheckFacade, **kwargs):
    """
    Update a healthcheck.
    """
    json_payload = {
        'healthcheck': {}
    }
    options = [
        'name', 'description', 'type', 'interval', 'force_ssl', 'checkport', 'http_method', 'http_uri', 'http_version',
        'http_host', 'http_expressionEnabled', 'http_expression', 'http_negate', 'http_value', 'tcp_enabled',
        'tcp_sendValue', 'tcp_matchType', 'tcp_negate', 'tcp_matchValue', 'agent_port', 'mysql_user',
        'mysql_post41', 'pgsql_user', 'smtp_domain', 'esmtp_domain', 'agentPort', 'dbUser', 'smtpDomain'
    ]
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['healthcheck'][option] = kwargs[option.lower()]

    result = haproxy_healthcheck_svc.update_healthcheck(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@healthcheck.command()
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
@pass_haproxy_healthcheck_svc
def delete(haproxy_healthcheck_svc: HaproxyHealthcheckFacade, **kwargs):
    """
    Delete healthcheck
    """
    result = haproxy_healthcheck_svc.delete_healthcheck(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
