import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats, int_as_string, tuple_to_csv
from opnsense_cli.commands.plugin.haproxy import haproxy
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.haproxy import Settings, Service
from opnsense_cli.facades.commands.plugin.haproxy.acl import HaproxyAclFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_haproxy_acl_svc = click.make_pass_decorator(HaproxyAclFacade)


@haproxy.group()
@pass_api_client
@click.pass_context
def acl(ctx, api_client: ApiClient, **kwargs):
    """
    Specify various conditions.

    Define custom rules for blocking malicious requests, choosing backends, redirecting to HTTPS and
    using cached objects.
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = HaproxyAclFacade(settings_api, service_api)


@acl.command()
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
        "uuid,name,description,expression,negate"
    ),
    show_default=True,
)
@pass_haproxy_acl_svc
def list(haproxy_acl_svc: HaproxyAclFacade, **kwargs):
    """
    Show all acl
    """
    result = haproxy_acl_svc.list_acls()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@acl.command()
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
        "name,description,expression,negate,hdr_beg,hdr_end,hdr,hdr_reg,hdr_sub,path_beg,path_end,path,path_reg,"
        "path_dir,path_sub,cust_hdr_beg_name,cust_hdr_beg,cust_hdr_end_name,cust_hdr_end,cust_hdr_name,cust_hdr,"
        "cust_hdr_reg_name,cust_hdr_reg,cust_hdr_sub_name,cust_hdr_sub,url_param,url_param_value,ssl_c_verify_code,"
        "ssl_c_ca_commonname,src,src_bytes_in_rate_comparison,src_bytes_in_rate,src_bytes_out_rate_comparison,"
        "src_bytes_out_rate,src_conn_cnt_comparison,src_conn_cnt,src_conn_cur_comparison,src_conn_cur,"
        "src_conn_rate_comparison,src_conn_rate,src_http_err_cnt_comparison,src_http_err_cnt,"
        "src_http_err_rate_comparison,src_http_err_rate,src_http_req_cnt_comparison,src_http_req_cnt,"
        "src_http_req_rate_comparison,src_http_req_rate,src_kbytes_in_comparison,src_kbytes_in,"
        "src_kbytes_out_comparison,src_kbytes_out,src_port_comparison,src_port,src_sess_cnt_comparison,"
        "src_sess_cnt,src_sess_rate_comparison,src_sess_rate,nbsrv,nbsrv_backend,BackendNrSrv,ssl_fc_sni,ssl_sni,"
        "ssl_sni_sub,ssl_sni_beg,ssl_sni_end,ssl_sni_reg,custom_acl,value,urlparam,"
        "queryBackend,BackendQuery,allowedUsers,Users,allowedGroups,Groups"
    ),
    show_default=True,
)
@pass_haproxy_acl_svc
def show(haproxy_acl_svc: HaproxyAclFacade, **kwargs):
    """
    Show details for acl
    """
    result = haproxy_acl_svc.show_acl(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@acl.command()
@click.argument('name')
@click.option(
    '--description',
    help=('Description for this condition.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--expression',
    help=('Type of condition'),
    type=click.Choice(
        [
            'http_auth', 'hdr_beg', 'hdr_end', 'hdr', 'hdr_reg', 'hdr_sub', 'path_beg', 'path_end', 'path',
            'path_reg', 'path_dir', 'path_sub', 'cust_hdr_beg', 'cust_hdr_end', 'cust_hdr', 'cust_hdr_reg',
            'cust_hdr_sub', 'url_param', 'ssl_c_verify', 'ssl_c_verify_code', 'ssl_c_ca_commonname', 'src',
            'src_is_local', 'src_port', 'src_bytes_in_rate', 'src_bytes_out_rate', 'src_kbytes_in', 'src_kbytes_out',
            'src_conn_cnt', 'src_conn_cur', 'src_conn_rate', 'src_http_err_cnt', 'src_http_err_rate',
            'src_http_req_cnt', 'src_http_req_rate', 'src_sess_cnt', 'src_sess_rate', 'nbsrv',
            'traffic_is_http', 'traffic_is_ssl', 'ssl_fc', 'ssl_fc_sni', 'ssl_sni', 'ssl_sni_sub',
            'ssl_sni_beg', 'ssl_sni_end', 'ssl_sni_reg', 'custom_acl'
        ]
    ),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None,
    required=True,
)
@click.option(
    '--negate/--no-negate',
    help=('Use this to invert the meaning of the expression.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--hdr_beg',
    help=('HTTP host header starts with string (prefix match)'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--hdr_end',
    help=('HTTP host header ends with string (suffix match)'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--hdr',
    help=('HTTP host header matches exact string'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--hdr_reg',
    help=('HTTP host header matches regular expression'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--hdr_sub',
    help=('HTTP host header contains string (substring match)'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--path_beg',
    help=('HTTP request URL path starts with string (prefix match)'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--path_end',
    help=('HTTP request URL path ends with string (suffix match)'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--path',
    help=('HTTP request URL path matches exact string'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--path_reg',
    help=('HTTP request URL path matches regular expression'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--path_dir',
    help=('HTTP request URL path contains directory (subdir match)'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--path_sub',
    help=('HTTP request URL path contains string (substring match)'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--cust_hdr_beg_name',
    help=('The name of the HTTP Header.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--cust_hdr_beg',
    help=('HTTP Header starts with string (prefix match)'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--cust_hdr_end_name',
    help=('The name of the HTTP Header.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--cust_hdr_end',
    help=('HTTP Header ends with string (suffix match)'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--cust_hdr_name',
    help=('The name of the HTTP Header.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--cust_hdr',
    help=('HTTP Header matches exact string'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--cust_hdr_reg_name',
    help=('The name of the HTTP Header.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--cust_hdr_reg',
    help=('HTTP Header matches regular expression'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--cust_hdr_sub_name',
    help=('The name of the HTTP Header.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--cust_hdr_sub',
    help=('HTTP Header contains string (substring match)'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--url_param',
    help=('Specify the URL parameter to be checked for the value specified below.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--url_param_value',
    help=('Specify the value for the URL parameter.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--ssl_c_verify_code',
    help=(
        'Specify the SSL/TLS error ID that should be checked for the incoming connection. '
        'Please refer to your SSL library\'s documentation for an exhaustive list of error codes.'
    ),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--ssl_c_ca_commonname',
    help=('Verify the CA Common-Name of the certificate presented by the client against the specified string.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--src',
    help=('Verify the source IPv4 address of the client of the session matches the specified IPv4 or IPv6 address.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--src_bytes_in_rate_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='gt',
    required=False,
)
@click.option(
    '--src_bytes_in_rate',
    help=('The average bytes rate from the incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--src_bytes_out_rate_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='gt',
    required=False,
)
@click.option(
    '--src_bytes_out_rate',
    help=('The average bytes rate to the incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--src_conn_cnt_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='gt',
    required=False,
)
@click.option(
    '--src_conn_cnt',
    help=('The cumulative number of connections initiated from the current incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--src_conn_cur_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='gt',
    required=False,
)
@click.option(
    '--src_conn_cur',
    help=(
        'The current amount of concurrent connections initiated from the current incoming connection\'s source address.'
    ),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--src_conn_rate_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='gt',
    required=False,
)
@click.option(
    '--src_conn_rate',
    help=('The average connection rate from the incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--src_http_err_cnt_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='gt',
    required=False,
)
@click.option(
    '--src_http_err_cnt',
    help=('The cumulative number of HTTP errors from the incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--src_http_err_rate_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='gt',
    required=False,
)
@click.option(
    '--src_http_err_rate',
    help=('The average rate of HTTP errors from the incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--src_http_req_cnt_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='gt',
    required=False,
)
@click.option(
    '--src_http_req_cnt',
    help=('The cumulative number of HTTP requests from the incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--src_http_req_rate_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='gt',
    required=False,
)
@click.option(
    '--src_http_req_rate',
    help=('The average rate of HTTP requests from the incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--src_kbytes_in_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='gt',
    required=False,
)
@click.option(
    '--src_kbytes_in',
    help=('The total amount of data received from the incoming connection\'s source address (in kilobytes).'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--src_kbytes_out_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='gt',
    required=False,
)
@click.option(
    '--src_kbytes_out',
    help=('The total amount of data sent to the incoming connection\'s source address (in kilobytes).'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--src_port_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='gt',
    required=False,
)
@click.option(
    '--src_port',
    help=(
        'An integer value corresponding to the TCP source port of the connection on the client side, '
        'which is the port the client connected from.'
    ),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--src_sess_cnt_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='gt',
    required=False,
)
@click.option(
    '--src_sess_cnt',
    help=('The cumulative number of connections initiated from the incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--src_sess_rate_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='gt',
    required=False,
)
@click.option(
    '--src_sess_rate',
    help=('None'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--nbsrv',
    help=('Verify the minimum number of usable servers in the named backend matches the specified value.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None,
    required=False,
)
@click.option(
    '--nbsrv_backend',
    help=('Use the specified backend to count usable servers. Leave empty to use the current backend.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--ssl_fc_sni',
    help=('The value of the Server Name TLS extension sent by a client matches the exact string.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--ssl_sni',
    help=('The value of the Server Name TLS extension sent by a client matches the exact string.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--ssl_sni_sub',
    help=(
        'The value of the Server Name TLS extension sent by a client contains the specified string (substring match).'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--ssl_sni_beg',
    help=(
        'The value of the Server Name TLS extension sent by a client starts with the specified string (prefix match).'
    ),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--ssl_sni_end',
    help=('The value of the Server Name TLS extension sent by a client ends with the specified string (suffix match).'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--ssl_sni_reg',
    help=('The value of the Server Name TLS extension sent by a client matches with the specified regular expression.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--custom_acl',
    help=('Specify a HAProxy condition/ACL that is currently not supported by the GUI.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--value',
    help=('None'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--urlparam',
    help=('None'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--queryBackend',
    help=('None'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--allowedUsers',
    help=('None'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--allowedGroups',
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
@pass_haproxy_acl_svc
def create(haproxy_acl_svc: HaproxyAclFacade, **kwargs):
    """
    Create a new acl
    """
    json_payload = {
        'acl': {
            "name": kwargs['name'],
            "description": kwargs['description'],
            "expression": kwargs['expression'],
            "negate": kwargs['negate'],
            "hdr_beg": kwargs['hdr_beg'],
            "hdr_end": kwargs['hdr_end'],
            "hdr": kwargs['hdr'],
            "hdr_reg": kwargs['hdr_reg'],
            "hdr_sub": kwargs['hdr_sub'],
            "path_beg": kwargs['path_beg'],
            "path_end": kwargs['path_end'],
            "path": kwargs['path'],
            "path_reg": kwargs['path_reg'],
            "path_dir": kwargs['path_dir'],
            "path_sub": kwargs['path_sub'],
            "cust_hdr_beg_name": kwargs['cust_hdr_beg_name'],
            "cust_hdr_beg": kwargs['cust_hdr_beg'],
            "cust_hdr_end_name": kwargs['cust_hdr_end_name'],
            "cust_hdr_end": kwargs['cust_hdr_end'],
            "cust_hdr_name": kwargs['cust_hdr_name'],
            "cust_hdr": kwargs['cust_hdr'],
            "cust_hdr_reg_name": kwargs['cust_hdr_reg_name'],
            "cust_hdr_reg": kwargs['cust_hdr_reg'],
            "cust_hdr_sub_name": kwargs['cust_hdr_sub_name'],
            "cust_hdr_sub": kwargs['cust_hdr_sub'],
            "url_param": kwargs['url_param'],
            "url_param_value": kwargs['url_param_value'],
            "ssl_c_verify_code": kwargs['ssl_c_verify_code'],
            "ssl_c_ca_commonname": kwargs['ssl_c_ca_commonname'],
            "src": kwargs['src'],
            "src_bytes_in_rate_comparison": kwargs['src_bytes_in_rate_comparison'],
            "src_bytes_in_rate": kwargs['src_bytes_in_rate'],
            "src_bytes_out_rate_comparison": kwargs['src_bytes_out_rate_comparison'],
            "src_bytes_out_rate": kwargs['src_bytes_out_rate'],
            "src_conn_cnt_comparison": kwargs['src_conn_cnt_comparison'],
            "src_conn_cnt": kwargs['src_conn_cnt'],
            "src_conn_cur_comparison": kwargs['src_conn_cur_comparison'],
            "src_conn_cur": kwargs['src_conn_cur'],
            "src_conn_rate_comparison": kwargs['src_conn_rate_comparison'],
            "src_conn_rate": kwargs['src_conn_rate'],
            "src_http_err_cnt_comparison": kwargs['src_http_err_cnt_comparison'],
            "src_http_err_cnt": kwargs['src_http_err_cnt'],
            "src_http_err_rate_comparison": kwargs['src_http_err_rate_comparison'],
            "src_http_err_rate": kwargs['src_http_err_rate'],
            "src_http_req_cnt_comparison": kwargs['src_http_req_cnt_comparison'],
            "src_http_req_cnt": kwargs['src_http_req_cnt'],
            "src_http_req_rate_comparison": kwargs['src_http_req_rate_comparison'],
            "src_http_req_rate": kwargs['src_http_req_rate'],
            "src_kbytes_in_comparison": kwargs['src_kbytes_in_comparison'],
            "src_kbytes_in": kwargs['src_kbytes_in'],
            "src_kbytes_out_comparison": kwargs['src_kbytes_out_comparison'],
            "src_kbytes_out": kwargs['src_kbytes_out'],
            "src_port_comparison": kwargs['src_port_comparison'],
            "src_port": kwargs['src_port'],
            "src_sess_cnt_comparison": kwargs['src_sess_cnt_comparison'],
            "src_sess_cnt": kwargs['src_sess_cnt'],
            "src_sess_rate_comparison": kwargs['src_sess_rate_comparison'],
            "src_sess_rate": kwargs['src_sess_rate'],
            "nbsrv": kwargs['nbsrv'],
            "nbsrv_backend": kwargs['nbsrv_backend'],
            "ssl_fc_sni": kwargs['ssl_fc_sni'],
            "ssl_sni": kwargs['ssl_sni'],
            "ssl_sni_sub": kwargs['ssl_sni_sub'],
            "ssl_sni_beg": kwargs['ssl_sni_beg'],
            "ssl_sni_end": kwargs['ssl_sni_end'],
            "ssl_sni_reg": kwargs['ssl_sni_reg'],
            "custom_acl": kwargs['custom_acl'],
            "value": kwargs['value'],
            "urlparam": kwargs['urlparam'],
            "queryBackend": kwargs['querybackend'],
            "allowedUsers": kwargs['allowedusers'],
            "allowedGroups": kwargs['allowedgroups'],
        }
    }

    result = haproxy_acl_svc.create_acl(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@acl.command()
@click.argument('uuid')
@click.option(
    '--name',
    help=('Name to identify this condition.'),
    show_default=True,
    default=None
)
@click.option(
    '--description',
    help=('Description for this condition.'),
    show_default=True,
    default=None
)
@click.option(
    '--expression',
    help=('None'),
    type=click.Choice(
        [
            'http_auth', 'hdr_beg', 'hdr_end', 'hdr', 'hdr_reg', 'hdr_sub', 'path_beg', 'path_end', 'path', 'path_reg',
            'path_dir', 'path_sub', 'cust_hdr_beg', 'cust_hdr_end', 'cust_hdr', 'cust_hdr_reg', 'cust_hdr_sub',
            'url_param', 'ssl_c_verify', 'ssl_c_verify_code', 'ssl_c_ca_commonname', 'src', 'src_is_local',
            'src_port', 'src_bytes_in_rate', 'src_bytes_out_rate', 'src_kbytes_in', 'src_kbytes_out',
            'src_conn_cnt', 'src_conn_cur', 'src_conn_rate', 'src_http_err_cnt', 'src_http_err_rate',
            'src_http_req_cnt', 'src_http_req_rate', 'src_sess_cnt', 'src_sess_rate', 'nbsrv', 'traffic_is_http',
            'traffic_is_ssl', 'ssl_fc', 'ssl_fc_sni', 'ssl_sni', 'ssl_sni_sub', 'ssl_sni_beg', 'ssl_sni_end',
            'ssl_sni_reg', 'custom_acl'
        ]
    ),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--negate/--no-negate',
    help=('Use this to invert the meaning of the expression.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--hdr_beg',
    help=('HTTP host header starts with string (prefix match)'),
    show_default=True,
    default=None
)
@click.option(
    '--hdr_end',
    help=('HTTP host header ends with string (suffix match)'),
    show_default=True,
    default=None
)
@click.option(
    '--hdr',
    help=('HTTP host header matches exact string'),
    show_default=True,
    default=None
)
@click.option(
    '--hdr_reg',
    help=('HTTP host header matches regular expression'),
    show_default=True,
    default=None
)
@click.option(
    '--hdr_sub',
    help=('HTTP host header contains string (substring match)'),
    show_default=True,
    default=None
)
@click.option(
    '--path_beg',
    help=('HTTP request URL path starts with string (prefix match)'),
    show_default=True,
    default=None
)
@click.option(
    '--path_end',
    help=('HTTP request URL path ends with string (suffix match)'),
    show_default=True,
    default=None
)
@click.option(
    '--path',
    help=('HTTP request URL path matches exact string'),
    show_default=True,
    default=None
)
@click.option(
    '--path_reg',
    help=('HTTP request URL path matches regular expression'),
    show_default=True,
    default=None
)
@click.option(
    '--path_dir',
    help=('HTTP request URL path contains directory (subdir match)'),
    show_default=True,
    default=None
)
@click.option(
    '--path_sub',
    help=('HTTP request URL path contains string (substring match)'),
    show_default=True,
    default=None
)
@click.option(
    '--cust_hdr_beg_name',
    help=('The name of the HTTP Header.'),
    show_default=True,
    default=None
)
@click.option(
    '--cust_hdr_beg',
    help=('HTTP Header starts with string (prefix match)'),
    show_default=True,
    default=None
)
@click.option(
    '--cust_hdr_end_name',
    help=('The name of the HTTP Header.'),
    show_default=True,
    default=None
)
@click.option(
    '--cust_hdr_end',
    help=('HTTP Header ends with string (suffix match)'),
    show_default=True,
    default=None
)
@click.option(
    '--cust_hdr_name',
    help=('The name of the HTTP Header.'),
    show_default=True,
    default=None
)
@click.option(
    '--cust_hdr',
    help=('HTTP Header matches exact string'),
    show_default=True,
    default=None
)
@click.option(
    '--cust_hdr_reg_name',
    help=('The name of the HTTP Header.'),
    show_default=True,
    default=None
)
@click.option(
    '--cust_hdr_reg',
    help=('HTTP Header matches regular expression'),
    show_default=True,
    default=None
)
@click.option(
    '--cust_hdr_sub_name',
    help=('The name of the HTTP Header.'),
    show_default=True,
    default=None
)
@click.option(
    '--cust_hdr_sub',
    help=('HTTP Header contains string (substring match)'),
    show_default=True,
    default=None
)
@click.option(
    '--url_param',
    help=('Specify the URL parameter to be checked for the value specified below.'),
    show_default=True,
    default=None
)
@click.option(
    '--url_param_value',
    help=('Specify the value for the URL parameter.'),
    show_default=True,
    default=None
)
@click.option(
    '--ssl_c_verify_code',
    help=(
        'Specify the SSL/TLS error ID that should be checked for the incoming connection. '
        'Please refer to your SSL library\'s documentation for an exhaustive list of error codes.'
    ),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--ssl_c_ca_commonname',
    help=('Verify the CA Common-Name of the certificate presented by the client against the specified string.'),
    show_default=True,
    default=None
)
@click.option(
    '--src',
    help=('Verify the source IPv4 address of the client of the session matches the specified IPv4 or IPv6 address.'),
    show_default=True,
    default=None
)
@click.option(
    '--src_bytes_in_rate_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--src_bytes_in_rate',
    help=('The average bytes rate from the incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--src_bytes_out_rate_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--src_bytes_out_rate',
    help=('The average bytes rate to the incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--src_conn_cnt_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--src_conn_cnt',
    help=('The cumulative number of connections initiated from the current incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--src_conn_cur_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--src_conn_cur',
    help=(
        'The current amount of concurrent connections initiated from the current incoming connection\'s source address.'
    ),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--src_conn_rate_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--src_conn_rate',
    help=('The average connection rate from the incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--src_http_err_cnt_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--src_http_err_cnt',
    help=('The cumulative number of HTTP errors from the incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--src_http_err_rate_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--src_http_err_rate',
    help=('The average rate of HTTP errors from the incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--src_http_req_cnt_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--src_http_req_cnt',
    help=('The cumulative number of HTTP requests from the incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--src_http_req_rate_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--src_http_req_rate',
    help=('The average rate of HTTP requests from the incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--src_kbytes_in_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--src_kbytes_in',
    help=('The total amount of data received from the incoming connection\'s source address (in kilobytes).'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--src_kbytes_out_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--src_kbytes_out',
    help=('The total amount of data sent to the incoming connection\'s source address (in kilobytes).'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--src_port_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--src_port',
    help=(
        'An integer value corresponding to the TCP source port of the connection on the client side, '
        'which is the port the client connected from.'
    ),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--src_sess_cnt_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--src_sess_cnt',
    help=('The cumulative number of connections initiated from the incoming connection\'s source address.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--src_sess_rate_comparison',
    help=('None'),
    type=click.Choice(['', 'gt', 'ge', 'eq', 'lt', 'le']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--src_sess_rate',
    help=('None'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--nbsrv',
    help=('Verify the minimum number of usable servers in the named backend matches the specified value.'),
    show_default=True,
    type=int,
    callback=int_as_string,
    default=None
)
@click.option(
    '--nbsrv_backend',
    help=('Use the specified backend to count usable servers. Leave empty to use the current backend.'),
    show_default=True,
    default=None
)
@click.option(
    '--ssl_fc_sni',
    help=('The value of the Server Name TLS extension sent by a client matches the exact string.'),
    show_default=True,
    default=None
)
@click.option(
    '--ssl_sni',
    help=('The value of the Server Name TLS extension sent by a client matches the exact string.'),
    show_default=True,
    default=None
)
@click.option(
    '--ssl_sni_sub',
    help=(
        'The value of the Server Name TLS extension sent by a client contains the specified string (substring match).'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--ssl_sni_beg',
    help=(
        'The value of the Server Name TLS extension sent by a client starts with the specified string (prefix match).'
    ),
    show_default=True,
    default=None
)
@click.option(
    '--ssl_sni_end',
    help=('The value of the Server Name TLS extension sent by a client ends with the specified string (suffix match).'),
    show_default=True,
    default=None
)
@click.option(
    '--ssl_sni_reg',
    help=('The value of the Server Name TLS extension sent by a client matches with the specified regular expression.'),
    show_default=True,
    default=None
)
@click.option(
    '--custom_acl',
    help=('Specify a HAProxy condition/ACL that is currently not supported by the GUI.'),
    show_default=True,
    default=None
)
@click.option(
    '--value',
    help=('None'),
    show_default=True,
    default=None
)
@click.option(
    '--urlparam',
    help=('None'),
    show_default=True,
    default=None
)
@click.option(
    '--queryBackend',
    help=('None'),
    show_default=True,
    default=None
)
@click.option(
    '--allowedUsers',
    help=('None'),
    show_default=True,
    default=None
)
@click.option(
    '--allowedGroups',
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
@pass_haproxy_acl_svc
def update(haproxy_acl_svc: HaproxyAclFacade, **kwargs):
    """
    Update a acl.
    """
    json_payload = {
        'acl': {}
    }
    options = [
        'name', 'description', 'expression', 'negate', 'hdr_beg', 'hdr_end', 'hdr', 'hdr_reg', 'hdr_sub', 'path_beg',
        'path_end', 'path', 'path_reg', 'path_dir', 'path_sub', 'cust_hdr_beg_name', 'cust_hdr_beg',
        'cust_hdr_end_name', 'cust_hdr_end', 'cust_hdr_name', 'cust_hdr', 'cust_hdr_reg_name', 'cust_hdr_reg',
        'cust_hdr_sub_name', 'cust_hdr_sub', 'url_param', 'url_param_value', 'ssl_c_verify_code', 'ssl_c_ca_commonname',
        'src', 'src_bytes_in_rate_comparison', 'src_bytes_in_rate', 'src_bytes_out_rate_comparison',
        'src_bytes_out_rate', 'src_conn_cnt_comparison', 'src_conn_cnt', 'src_conn_cur_comparison', 'src_conn_cur',
        'src_conn_rate_comparison', 'src_conn_rate', 'src_http_err_cnt_comparison', 'src_http_err_cnt',
        'src_http_err_rate_comparison', 'src_http_err_rate', 'src_http_req_cnt_comparison', 'src_http_req_cnt',
        'src_http_req_rate_comparison', 'src_http_req_rate', 'src_kbytes_in_comparison', 'src_kbytes_in',
        'src_kbytes_out_comparison', 'src_kbytes_out', 'src_port_comparison', 'src_port', 'src_sess_cnt_comparison',
        'src_sess_cnt', 'src_sess_rate_comparison', 'src_sess_rate', 'nbsrv', 'nbsrv_backend', 'ssl_fc_sni', 'ssl_sni',
        'ssl_sni_sub', 'ssl_sni_beg', 'ssl_sni_end', 'ssl_sni_reg', 'custom_acl', 'value', 'urlparam', 'queryBackend',
        'allowedUsers', 'allowedGroups'
    ]
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['acl'][option] = kwargs[option.lower()]

    result = haproxy_acl_svc.update_acl(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@acl.command()
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
@pass_haproxy_acl_svc
def delete(haproxy_acl_svc: HaproxyAclFacade, **kwargs):
    """
    Delete acl
    """
    result = haproxy_acl_svc.delete_acl(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
