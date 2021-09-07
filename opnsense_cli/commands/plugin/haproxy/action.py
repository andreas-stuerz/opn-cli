import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, available_formats, int_as_string, tuple_to_csv
from opnsense_cli.commands.plugin.haproxy import haproxy
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.haproxy import Settings, Service
from opnsense_cli.facades.commands.plugin.haproxy.action import HaproxyActionFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_haproxy_action_svc = click.make_pass_decorator(HaproxyActionFacade)


@haproxy.group()
@pass_api_client
@click.pass_context
def action(ctx, api_client: ApiClient, **kwargs):
    """
    Perform a set of actions if one or more conditions match.
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = HaproxyActionFacade(settings_api, service_api)


@action.command()
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
        "uuid,name,description,testType,Acls,operator,type"
    ),
    show_default=True,
)
@pass_haproxy_action_svc
def list(haproxy_action_svc: HaproxyActionFacade, **kwargs):
    """
    Show all action
    """
    result = haproxy_action_svc.list_actions()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@action.command()
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
        "name,description,testType,linkedAcls,Acls,operator,type,use_backend,Backend,use_server,Server,"
        "http_request_auth,http_request_redirect,http_request_lua,http_request_use_service,"
        "http_request_add_header_name,"
        "http_request_add_header_content,http_request_set_header_name,http_request_set_header_content,"
        "http_request_del_header_name,http_request_replace_header_name,http_request_replace_header_regex,"
        "http_request_replace_value_name,http_request_replace_value_regex,http_request_set_path,"
        "http_request_set_var_scope,http_request_set_var_name,http_request_set_var_expr,"
        "http_response_lua,http_response_add_header_name,http_response_add_header_content,"
        "http_response_set_header_name,http_response_set_header_content,http_response_del_header_name,"
        "http_response_replace_header_name,http_response_replace_header_regex,http_response_replace_value_name,"
        "http_response_replace_value_regex,http_response_set_status_code,http_response_set_status_reason,"
        "http_response_set_var_scope,http_response_set_var_name,http_response_set_var_expr,tcp_request_content_lua,"
        "tcp_request_content_use_service,tcp_request_inspect_delay,tcp_response_content_lua,tcp_response_inspect_delay,"
        "custom,useBackend,Backends,useServer,Servers,actionName,actionFind,actionValue,map_use_backend_file,Mapfile,"
        "map_use_backend_default,BackendDefault"
    ),
    show_default=True,
)
@pass_haproxy_action_svc
def show(haproxy_action_svc: HaproxyActionFacade, **kwargs):
    """
    Show details for action
    """
    result = haproxy_action_svc.show_action(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@action.command()
@click.argument('name')
@click.option(
    '--description',
    help=('Description for this rule.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--testType',
    help=(
        'Choose how to test. By using IF it tests if the condition evaluates to true. '
        'If you use UNLESS, the sense of the test is reversed.'
    ),
    type=click.Choice(['if', 'unless']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='if',
    required=True,
)
@click.option(
    '--linkedAcls',
    help=('Select one or more conditions to be used for this rule.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--operator',
    help=('Choose a logical operator.'),
    type=click.Choice(['', 'and', 'or']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='and',
    required=False,
)
@click.option(
    '--type',
    help=('Choose a HAProxy function that should be executed if the condition evaluates to true.'),
    type=click.Choice(
        [
            'use_backend', 'use_server', 'map_use_backend', 'http-request_allow', 'http-request_deny',
            'http-request_tarpit', 'http-request_auth', 'http-request_redirect', 'http-request_lua',
            'http-request_use-service', 'http-request_add-header', 'http-request_set-header', 'http-request_del-header',
            'http-request_replace-header', 'http-request_replace-value', 'http-request_set-path',
            'http-request_set-var', 'http-response_allow', 'http-response_deny', 'http-response_lua',
            'http-response_add-header', 'http-response_set-header', 'http-response_del-header',
            'http-response_replace-header', 'http-response_replace-value', 'http-response_set-status',
            'http-response_set-var', 'tcp-request_connection_accept', 'tcp-request_connection_reject',
            'tcp-request_content_accept', 'tcp-request_content_reject', 'tcp-request_content_lua',
            'tcp-request_content_use-service', 'tcp-request_inspect-delay', 'tcp-response_content_accept',
            'tcp-response_content_close', 'tcp-response_content_reject', 'tcp-response_content_lua',
            'tcp-response_inspect-delay', 'custom'
        ]
    ),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None,
    required=True,
)
@click.option(
    '--use_backend',
    help=('HAProxy will use this backend pool if the condition evaluates to true.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--use_server',
    help=(
        'HAProxy will use this server instead of other servers that are specified in the Backend Pool. '
        'The server must exist in the context where this rule is applied.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_request_auth',
    help=(
        'When HAProxy requests user name and password from the user, this optional authentication realm is returned '
        'with the response (typically the application\'s name).'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_request_redirect',
    help=(
        'Use HAProxy\'s redirect function to return a HTTP redirection.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_request_lua',
    help=('Execute the specified Lua function. You will most likely need to include/load your Lua code first.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_request_use_service',
    help=('Register the specified Lua service. You will most likely need to include/load your Lua code first.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_request_add_header_name',
    help=('Append a HTTP header field with the specified name.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_request_add_header_content',
    help=(
        'The value that should be set for the specified HTTP header. '
        'Note that it is possible to use pre-defined variables.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_request_set_header_name',
    help=(
        'Remove the HTTP header field with the specified name and add a new one with the same name. '
        'This is useful when passing security information to the server, '
        'where the header must not be manipulated by external users.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_request_set_header_content',
    help=(
        'The value that should be set for the specified HTTP header.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_request_del_header_name',
    help=('Remove the HTTP header field with the specified name.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_request_replace_header_name',
    help=('The name of the HTTP header field.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_request_replace_header_regex',
    help=('Matches the specified regular expression in all occurrences of the header field.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_request_replace_value_name',
    help=('The name of the HTTP header field.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_request_replace_value_regex',
    help=(
        'This is suited for all header fields which are allowed to carry more than one value: '
        'Matches the specified regular expression against every comma-delimited value of the header field.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_request_set_path',
    help=(
        'Rewrites the request path. The query string, if any, is left intact. '
        'If a scheme and authority is found before the path, they are left intact as well.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_request_set_var_scope',
    help=('The name of the variable starts with an indication about its scope.'),
    type=click.Choice(['', 'proc', 'sess', 'txn', 'req', 'res']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='txn',
    required=False,
)
@click.option(
    '--http_request_set_var_name',
    help=('None'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_request_set_var_expr',
    help=('A standard HAProxy expression formed by a sample-fetch followed by some converters.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_response_lua',
    help=('Execute the specified Lua function. You will most likely need to include/load your Lua code first.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_response_add_header_name',
    help=('Append a HTTP header field with the specified name.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_response_add_header_content',
    help=(
        'The value that should be set for the specified HTTP header. '
        'Note that it\'s possible to use pre-defined variables'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_response_set_header_name',
    help=(
        'Remove the HTTP header field with the specified name and add a new one with the same name. '
        'This is useful when passing security information to the server, '
        'where the header must not be manipulated by external users.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_response_set_header_content',
    help=(
        'The value that should be set for the specified HTTP header. '
        'Note that it\'s possible to use pre-defined variables'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_response_del_header_name',
    help=('Remove the HTTP header field with the specified name.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_response_replace_header_name',
    help=('The name of the HTTP header field.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_response_replace_header_regex',
    help=('Matches the specified regular expression in all occurrences of header field.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_response_replace_value_name',
    help=('The name of the HTTP header field.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_response_replace_value_regex',
    help=(
        'This is suited for all header fields which are allowed to carry more than one value: '
        'Matches the specified regular expression against every comma-delimited value of the header field.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_response_set_status_code',
    help=('Replaces the response status code. Must be an integer between 100 and 999.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--http_response_set_status_reason',
    help=(
        'An optional custom reason text for the HTTP status code. '
        'If empty the default reason for the specified code will be used.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_response_set_var_scope',
    help=('The name of the variable starts with an indication about its scope.'),
    type=click.Choice(['', 'proc', 'sess', 'txn', 'req', 'res']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='txn',
    required=False,
)
@click.option(
    '--http_response_set_var_name',
    help=('None'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--http_response_set_var_expr',
    help=('A standard HAProxy expression formed by a sample-fetch followed by some converters.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tcp_request_content_lua',
    help=('Execute the specified Lua function. You will most likely need to include/load your Lua code first.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tcp_request_content_use_service',
    help=('Register the specified Lua service. You will most likely need to include/load your Lua code first.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tcp_request_inspect_delay',
    help=(
        'Set the maximum allowed time to wait for data during content inspection. '
        'Defaults to milliseconds. You may also enter a number followed by one of the supported suffixes '
        '"d" (days), "h" (hour), "m" (minute), "s" (seconds), "ms" (miliseconds).'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tcp_response_content_lua',
    help=('Execute the specified Lua function. You will most likely need to include/load your Lua code first.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--tcp_response_inspect_delay',
    help=(
        'Set the maximum allowed time to wait for a response during content inspection. '
        'Defaults to milliseconds. You may also enter a number followed by one of the supported suffixes '
        '"d" (days), "h" (hour), "m" (minute), "s" (seconds), "ms" (miliseconds).'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--custom',
    help=('Specify a HAProxy rule/ACL that is currently not supported by the GUI.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--useBackend',
    help=('None'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--useServer',
    help=('None'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--actionName',
    help=('None'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--actionFind',
    help=('None'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--actionValue',
    help=('None'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--map_use_backend_file',
    help=(
        'HAProxy will extract the Host header from the HTTP request and search the map file for a match. '
        'If a match is found, the backend pool from the map file will be used.'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--map_use_backend_default',
    help=('HAProxy will use this backend pool if no match is found in the map file.'),
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
@pass_haproxy_action_svc
def create(haproxy_action_svc: HaproxyActionFacade, **kwargs):
    """
    Create a new action
    """
    json_payload = {
        'action': {
            "name": kwargs['name'],
            "description": kwargs['description'],
            "testType": kwargs['testtype'],
            "linkedAcls": kwargs['linkedacls'],
            "operator": kwargs['operator'],
            "type": kwargs['type'],
            "use_backend": kwargs['use_backend'],
            "use_server": kwargs['use_server'],
            "http_request_auth": kwargs['http_request_auth'],
            "http_request_redirect": kwargs['http_request_redirect'],
            "http_request_lua": kwargs['http_request_lua'],
            "http_request_use_service": kwargs['http_request_use_service'],
            "http_request_add_header_name": kwargs['http_request_add_header_name'],
            "http_request_add_header_content": kwargs['http_request_add_header_content'],
            "http_request_set_header_name": kwargs['http_request_set_header_name'],
            "http_request_set_header_content": kwargs['http_request_set_header_content'],
            "http_request_del_header_name": kwargs['http_request_del_header_name'],
            "http_request_replace_header_name": kwargs['http_request_replace_header_name'],
            "http_request_replace_header_regex": kwargs['http_request_replace_header_regex'],
            "http_request_replace_value_name": kwargs['http_request_replace_value_name'],
            "http_request_replace_value_regex": kwargs['http_request_replace_value_regex'],
            "http_request_set_path": kwargs['http_request_set_path'],
            "http_request_set_var_scope": kwargs['http_request_set_var_scope'],
            "http_request_set_var_name": kwargs['http_request_set_var_name'],
            "http_request_set_var_expr": kwargs['http_request_set_var_expr'],
            "http_response_lua": kwargs['http_response_lua'],
            "http_response_add_header_name": kwargs['http_response_add_header_name'],
            "http_response_add_header_content": kwargs['http_response_add_header_content'],
            "http_response_set_header_name": kwargs['http_response_set_header_name'],
            "http_response_set_header_content": kwargs['http_response_set_header_content'],
            "http_response_del_header_name": kwargs['http_response_del_header_name'],
            "http_response_replace_header_name": kwargs['http_response_replace_header_name'],
            "http_response_replace_header_regex": kwargs['http_response_replace_header_regex'],
            "http_response_replace_value_name": kwargs['http_response_replace_value_name'],
            "http_response_replace_value_regex": kwargs['http_response_replace_value_regex'],
            "http_response_set_status_code": kwargs['http_response_set_status_code'],
            "http_response_set_status_reason": kwargs['http_response_set_status_reason'],
            "http_response_set_var_scope": kwargs['http_response_set_var_scope'],
            "http_response_set_var_name": kwargs['http_response_set_var_name'],
            "http_response_set_var_expr": kwargs['http_response_set_var_expr'],
            "tcp_request_content_lua": kwargs['tcp_request_content_lua'],
            "tcp_request_content_use_service": kwargs['tcp_request_content_use_service'],
            "tcp_request_inspect_delay": kwargs['tcp_request_inspect_delay'],
            "tcp_response_content_lua": kwargs['tcp_response_content_lua'],
            "tcp_response_inspect_delay": kwargs['tcp_response_inspect_delay'],
            "custom": kwargs['custom'],
            "useBackend": kwargs['usebackend'],
            "useServer": kwargs['useserver'],
            "actionName": kwargs['actionname'],
            "actionFind": kwargs['actionfind'],
            "actionValue": kwargs['actionvalue'],
            "map_use_backend_file": kwargs['map_use_backend_file'],
            "map_use_backend_default": kwargs['map_use_backend_default'],
        }
    }

    result = haproxy_action_svc.create_action(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@action.command()
@click.argument('uuid')
@click.option(
    '--name',
    help=('Name to identify this rule.'),
    show_default=True,
    default=None
)
@click.option(
    '--description',
    help=('Description for this rule.'),
    show_default=True,
    default=None
)
@click.option(
    '--testType',
    help=(
        'Choose how to test. By using IF it tests if the condition evaluates to true. '
        'If you use UNLESS, the sense of the test is reversed.'
    ),
    type=click.Choice(['if', 'unless']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--linkedAcls',
    help=('Select one or more conditions to be used for this rule.'),
    show_default=True,
    default=None
)
@click.option(
    '--operator',
    help=('Choose a logical operator.'),
    type=click.Choice(['', 'and', 'or']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--type',
    help=('Choose a HAProxy function that should be executed if the condition evaluates to true.'),
    type=click.Choice(
        [
            'use_backend', 'use_server', 'map_use_backend', 'http-request_allow', 'http-request_deny',
            'http-request_tarpit', 'http-request_auth', 'http-request_redirect', 'http-request_lua',
            'http-request_use-service', 'http-request_add-header', 'http-request_set-header',
            'http-request_del-header', 'http-request_replace-header', 'http-request_replace-value',
            'http-request_set-path', 'http-request_set-var', 'http-response_allow', 'http-response_deny',
            'http-response_lua', 'http-response_add-header', 'http-response_set-header', 'http-response_del-header',
            'http-response_replace-header', 'http-response_replace-value', 'http-response_set-status',
            'http-response_set-var', 'tcp-request_connection_accept', 'tcp-request_connection_reject',
            'tcp-request_content_accept', 'tcp-request_content_reject', 'tcp-request_content_lua',
            'tcp-request_content_use-service', 'tcp-request_inspect-delay', 'tcp-response_content_accept',
            'tcp-response_content_close', 'tcp-response_content_reject', 'tcp-response_content_lua',
            'tcp-response_inspect-delay', 'custom'
        ]
    ),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--use_backend',
    help=('HAProxy will use this backend pool if the condition evaluates to true.'),
    show_default=True,
    default=None
)
@click.option(
    '--use_server',
    help=(
        'HAProxy will use this server instead of other servers that are specified in the Backend Pool. '
        'The server must exist in the context where this rule is applied.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--http_request_auth',
    help=(
        'When HAProxy requests user name and password from the user, this optional authentication realm '
        'is returned with the response (typically the application\'s name).'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--http_request_redirect',
    help=(
        'Use HAProxy\'s redirect function to return a HTTP redirection.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--http_request_lua',
    help=('Execute the specified Lua function. You will most likely need to include/load your Lua code first.'),
    show_default=True,
    default=None
)
@click.option(
    '--http_request_use_service',
    help=('Register the specified Lua service. You will most likely need to include/load your Lua code first.'),
    show_default=True,
    default=None
)
@click.option(
    '--http_request_add_header_name',
    help=('Append a HTTP header field with the specified name.'),
    show_default=True,
    default=None
)
@click.option(
    '--http_request_add_header_content',
    help=(
        'The value that should be set for the specified HTTP header. '
        'Note that it is possible to use pre-defined variables.'),
    show_default=True,
    default=None
)
@click.option(
    '--http_request_set_header_name',
    help=(
        'Remove the HTTP header field with the specified name and add a new one with the same name. '
        'This is useful when passing security information to the server, '
        'where the header must not be manipulated by external users.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--http_request_set_header_content',
    help=(
        'The value that should be set for the specified HTTP header. '
        'Note that it\'s possible to use pre-defined variables.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--http_request_del_header_name',
    help=('Remove the HTTP header field with the specified name.'),
    show_default=True,
    default=None
)
@click.option(
    '--http_request_replace_header_name',
    help=('The name of the HTTP header field.'),
    show_default=True,
    default=None
)
@click.option(
    '--http_request_replace_header_regex',
    help=('Matches the specified regular expression in all occurrences of the header field.'),
    show_default=True,
    default=None
)
@click.option(
    '--http_request_replace_value_name',
    help=('The name of the HTTP header field.'),
    show_default=True,
    default=None
)
@click.option(
    '--http_request_replace_value_regex',
    help=(
        'This is suited for all header fields which are allowed to carry more than one value: '
        'Matches the specified regular expression against every comma-delimited value of the header field.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--http_request_set_path',
    help=(
        'Rewrites the request path. The query string, if any, is left intact. '
        'If a scheme and authority is found before the path, they are left intact as well.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--http_request_set_var_scope',
    help=('The name of the variable starts with an indication about its scope.'),
    type=click.Choice(['', 'proc', 'sess', 'txn', 'req', 'res']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--http_request_set_var_name',
    help=('None'),
    show_default=True,
    default=None
)
@click.option(
    '--http_request_set_var_expr',
    help=('A standard HAProxy expression formed by a sample-fetch followed by some converters.'),
    show_default=True,
    default=None
)
@click.option(
    '--http_response_lua',
    help=('Execute the specified Lua function. You will most likely need to include/load your Lua code first.'),
    show_default=True,
    default=None
)
@click.option(
    '--http_response_add_header_name',
    help=('Append a HTTP header field with the specified name.'),
    show_default=True,
    default=None
)
@click.option(
    '--http_response_add_header_content',
    help=(
        'The value that should be set for the specified HTTP header. '
        'Note that it\'s possible to use pre-defined variables.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--http_response_set_header_name',
    help=(
        'Remove the HTTP header field with the specified name and add a new one with the same name. '
        'This is useful when passing security information to the server, '
        'where the header must not be manipulated by external users.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--http_response_set_header_content',
    help=(
        'The value that should be set for the specified HTTP header. '
        'Note that it\'s possible to use pre-defined variables.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--http_response_del_header_name',
    help=('Remove the HTTP header field with the specified name.'),
    show_default=True,
    default=None
)
@click.option(
    '--http_response_replace_header_name',
    help=('The name of the HTTP header field.'),
    show_default=True,
    default=None
)
@click.option(
    '--http_response_replace_header_regex',
    help=('Matches the specified regular expression in all occurrences of header field.'),
    show_default=True,
    default=None
)
@click.option(
    '--http_response_replace_value_name',
    help=('The name of the HTTP header field.'),
    show_default=True,
    default=None
)
@click.option(
    '--http_response_replace_value_regex',
    help=(
        'This is suited for all header fields which are allowed to carry more than one value: '
        'Matches the specified regular expression against every comma-delimited value of the header field.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--http_response_set_status_code',
    help=('Replaces the response status code. Must be an integer between 100 and 999.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--http_response_set_status_reason',
    help=(
        'An optional custom reason text for the HTTP status code. '
        'If empty the default reason for the specified code will be used.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--http_response_set_var_scope',
    help=('The name of the variable starts with an indication about its scope.'),
    type=click.Choice(['', 'proc', 'sess', 'txn', 'req', 'res']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--http_response_set_var_name',
    help=('None'),
    show_default=True,
    default=None
)
@click.option(
    '--http_response_set_var_expr',
    help=('A standard HAProxy expression formed by a sample-fetch followed by some converters.'),
    show_default=True,
    default=None
)
@click.option(
    '--tcp_request_content_lua',
    help=('Execute the specified Lua function. You will most likely need to include/load your Lua code first.'),
    show_default=True,
    default=None
)
@click.option(
    '--tcp_request_content_use_service',
    help=('Register the specified Lua service. You will most likely need to include/load your Lua code first.'),
    show_default=True,
    default=None
)
@click.option(
    '--tcp_request_inspect_delay',
    help=(
        'Set the maximum allowed time to wait for data during content inspection. '
        'Defaults to milliseconds. You may also enter a number followed by one of the supported suffixes '
        '"d" (days), "h" (hour), "m" (minute), "s" (seconds), "ms" (miliseconds).'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--tcp_response_content_lua',
    help=('Execute the specified Lua function. You will most likely need to include/load your Lua code first.'),
    show_default=True,
    default=None
)
@click.option(
    '--tcp_response_inspect_delay',
    help=(
        'Set the maximum allowed time to wait for a response during content inspection. '
        'Defaults to milliseconds. You may also enter a number followed by one of the supported suffixes '
        '"d" (days), "h" (hour), "m" (minute), "s" (seconds), "ms" (miliseconds).'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--custom',
    help=('Specify a HAProxy rule/ACL that is currently not supported by the GUI.'),
    show_default=True,
    default=None
)
@click.option(
    '--useBackend',
    help=('None'),
    show_default=True,
    default=None
)
@click.option(
    '--useServer',
    help=('None'),
    show_default=True,
    default=None
)
@click.option(
    '--actionName',
    help=('None'),
    show_default=True,
    default=None
)
@click.option(
    '--actionFind',
    help=('None'),
    show_default=True,
    default=None
)
@click.option(
    '--actionValue',
    help=('None'),
    show_default=True,
    default=None
)
@click.option(
    '--map_use_backend_file',
    help=(
        'HAProxy will extract the Host header from the HTTP request and search the map file for a match. '
        'If a match is found, the backend pool from the map file will be used.'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--map_use_backend_default',
    help=('HAProxy will use this backend pool if no match is found in the map file.'),
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
@pass_haproxy_action_svc
def update(haproxy_action_svc: HaproxyActionFacade, **kwargs):
    """
    Update a action.
    """
    json_payload = {
        'action': {}
    }
    options = [
        'name', 'description', 'testType', 'linkedAcls', 'operator', 'type', 'use_backend', 'use_server',
        'http_request_auth', 'http_request_redirect', 'http_request_lua', 'http_request_use_service',
        'http_request_add_header_name', 'http_request_add_header_content', 'http_request_set_header_name',
        'http_request_set_header_content', 'http_request_del_header_name', 'http_request_replace_header_name',
        'http_request_replace_header_regex', 'http_request_replace_value_name', 'http_request_replace_value_regex',
        'http_request_set_path', 'http_request_set_var_scope', 'http_request_set_var_name',
        'http_request_set_var_expr', 'http_response_lua', 'http_response_add_header_name',
        'http_response_add_header_content', 'http_response_set_header_name', 'http_response_set_header_content',
        'http_response_del_header_name', 'http_response_replace_header_name', 'http_response_replace_header_regex',
        'http_response_replace_value_name', 'http_response_replace_value_regex', 'http_response_set_status_code',
        'http_response_set_status_reason', 'http_response_set_var_scope', 'http_response_set_var_name',
        'http_response_set_var_expr', 'tcp_request_content_lua', 'tcp_request_content_use_service',
        'tcp_request_inspect_delay', 'tcp_response_content_lua', 'tcp_response_inspect_delay',
        'custom', 'useBackend', 'useServer', 'actionName', 'actionFind', 'actionValue',
        'map_use_backend_file', 'map_use_backend_default'
    ]
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['action'][option] = kwargs[option.lower()]

    result = haproxy_action_svc.update_action(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@action.command()
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
@pass_haproxy_action_svc
def delete(haproxy_action_svc: HaproxyActionFacade, **kwargs):
    """
    Delete action
    """
    result = haproxy_action_svc.delete_action(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
