import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, expand_path, comma_to_newline, available_formats
from opnsense_cli.commands.haproxy import haproxy
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.haproxy import Settings, Export
from opnsense_cli.facades.haproxy.config import HaproxyConfigFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_haproxy_config_svc = click.make_pass_decorator(HaproxyConfigFacade)


@haproxy.group()
@pass_api_client
@click.pass_context
def config(ctx, api_client: ApiClient, **kwargs):
    """
    Manage haproxy configuration
    """
    settings_api = Settings(api_client)
    export_api = Export(api_client)
    ctx.obj = HaproxyConfigFacade(settings_api, export_api)


@config.command()
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
    default="response",
    show_default=True,
)
@pass_haproxy_config_svc
def show(haproxy_server_svc: HaproxyConfigFacade, **kwargs):
    """
    Show the running haproxy config
    """
    result = haproxy_server_svc.show_config()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()

@config.command()
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
    default="response",
    show_default=True,
)
@pass_haproxy_config_svc
def diff(haproxy_server_svc: HaproxyConfigFacade, **kwargs):
    """
    Diff of running and staging config
    """
    result = haproxy_server_svc.show_diff()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@config.command()
@click.option(
    '-p','--path',
    help='The target path.',
    type=click.Path(dir_okay=False),
    default='./haproxy_config_export.zip',
    is_eager=True,
    show_default=True,
    callback=expand_path,
    show_envvar=True,
    required=True,
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
    default="status",
    show_default=True,
)
@pass_haproxy_config_svc
def download(haproxy_server_svc: HaproxyConfigFacade, **kwargs):
    """
    Download complete haproxy config as zip
    """
    result = haproxy_server_svc.download_config(kwargs['path'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


# @config.command()
# @click.argument('server_name')
# @click.option(
#     '--output', '-o',
#     help='Specifies the Output format.',
#     default="table",
#     type=click.Choice(available_formats()),
#     callback=formatter_from_formatter_name,
#     show_default=True,
# )
# @click.option(
#     '--cols', '-c',
#     help='Which columns should be printed? Pass empty string (-c '') to show all columns',
#     default="ip",
#     show_default=True,
# )
# @pass_haproxy_config_svc
# def table(firewall_server_svc: FirewallAliasFacade, **kwargs):
#     """
#     Show pf table entries for server
#     """
#     result = firewall_server_svc.show_pf_table(kwargs['server_name'])
#
#     CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
#
#
# @config.command()
# @click.argument('name')
# @click.option(
#     '--type', '-t',
#     help='The server type',
#     type=click.Choice(['host', 'network', 'port', 'url', 'urltable', 'geoip', 'networkgroup', 'mac', 'external']),
#     show_default=True,
#     required=True,
# )
# @click.option(
#     '--content', '-C',
#     help='The server content. Pass multiple values comma separated. Exclusion starts with “!” sign eg. !192.168.0.0/24',
#     show_default=True,
#     callback=comma_to_newline,
#     required=True,
# )
# @click.option(
#     '--description', '-d',
#     help='The server description.',
#     show_default=True,
#     required=True,
# )
# @click.option(
#     '--enabled/--disabled',
#     help='Enable or disable server.',
#     show_default=True,
#     is_flag=True,
#     callback=bool_as_string,
#     default=True,
# )
# @click.option(
#     '--proto', '-p',
#     help='Which ip type should be used? IPv4 and/or IPv6 networks?',
#     type=click.Choice(['', 'IPv4', 'IPv6', 'IPv4,IPv6']),
#     show_default=True,
# )
# @click.option(
#     '--updatefreq', '-u',
#     help='How often should the server type url_table be updated in days? For every hour specify 1/24: 0.0416666666',
#     type=float,
#     show_default=True,
# )
# @click.option(
#     '--counters/--no-counters',
#     help='Enable or disable pfTable statistics for this server.',
#     show_default=True,
#     is_flag=True,
#     default=False,
# )
# @click.option(
#     '--output', '-o',
#     help='Specifies the Output format.',
#     default="plain",
#     type=click.Choice(available_formats()),
#     callback=formatter_from_formatter_name,
#     show_default=True,
# )
# @click.option(
#     '--cols', '-c',
#     help='Which columns should be printed? Pass empty string (-c '') to show all columns',
#     default="result,validations",
#     show_default=True,
# )
# @pass_haproxy_config_svc
# def create(firewall_server_svc: FirewallAliasFacade, **kwargs):
#     """
#     Create a new server.
#
#     See: https://wiki.opnsense.org/manual/serveres.html
#     """
#     json_payload = {
#         'server': {
#             "enabled": kwargs['enabled'],
#             "name": kwargs['name'],
#             "type": kwargs['type'],
#             "content": kwargs['content'],
#             "description": kwargs['description'],
#             "proto": kwargs['proto'],
#             "updatefreq": kwargs['updatefreq'],
#             "counters": kwargs['counters'],
#         }
#     }
#
#     result = firewall_server_svc.create_server(json_payload)
#
#     CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
#
#
# @config.command()
# @click.argument('server_name')
# @click.option(
#     '--name', '-n',
#     help='The new name for the server.',
#     show_default=True,
# )
# @click.option(
#     '--type', '-t',
#     help='The server type',
#     type=click.Choice(['host', 'network', 'port', 'url', 'urltable', 'geoip', 'networkgroup', 'mac', 'external']),
#     show_default=True,
# )
# @click.option(
#     '--content', '-C',
#     help='The server content. Pass multiple values comma separated. Exclusion starts with “!” sign eg. !192.168.0.0/24',
#     show_default=True,
#     callback=comma_to_newline,
# )
# @click.option(
#     '--description', '-d',
#     help='The server description.',
#     show_default=True,
# )
# @click.option(
#     '--enabled/--disabled',
#     help='Enable or disable server.',
#     show_default=True,
#     is_flag=True,
#     callback=bool_as_string,
#     default=None,
# )
# @click.option(
#     '--enabled/--disabled',
#     help='Enable or disable server.',
#     show_default=True,
#     is_flag=True,
#     default=None
# )
# @click.option(
#     '--proto', '-p',
#     help='Which ip type should be used? IPv4 and/or IPv6 networks?',
#     type=click.Choice(['', 'IPv4', 'IPv6', 'IPv4,IPv6']),
#     show_default=True,
# )
# @click.option(
#     '--updatefreq', '-u',
#     help='How often should the server type url_table be updated in days? For every hour specify 1/24: 0.0416666666',
#     type=float,
#     show_default=True,
# )
# @click.option(
#     '--counters/--no-counters',
#     help='Enable or disable pfTable statistics for this server.',
#     show_default=True,
#     is_flag=True,
#     default=None
# )
# @click.option(
#     '--output', '-o',
#     help='Specifies the Output format.',
#     default="plain",
#     type=click.Choice(available_formats()),
#     callback=formatter_from_formatter_name,
#     show_default=True,
# )
# @click.option(
#     '--cols', '-c',
#     help='Which columns should be printed? Pass empty string (-c '') to show all columns',
#     default="result,validations",
#     show_default=True,
# )
# @pass_haproxy_config_svc
# def update(firewall_server_svc: FirewallAliasFacade, **kwargs):
#     """
#     Update an server.
#
#     See: https://wiki.opnsense.org/manual/serveres.html
#     """
#     json_payload = {
#         'server': {'name': kwargs['server_name']}
#     }
#     options = [
#         'enabled', 'name', 'type', 'content', 'description', 'proto', 'updatefreq', 'counters'
#     ]
#     for option in options:
#         if kwargs[option] is not None:
#             json_payload['server'][option] = kwargs[option]
#
#     result = firewall_server_svc.update_server(kwargs['server_name'], json_payload)
#
#     CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
#
#
# @config.command()
# @click.argument('name')
# @click.option(
#     '--output', '-o',
#     help='Specifies the Output format.',
#     default="plain",
#     type=click.Choice(available_formats()),
#     callback=formatter_from_formatter_name,
#     show_default=True,
# )
# @click.option(
#     '--cols', '-c',
#     help='Which columns should be printed? Pass empty string (-c '') to show all columns',
#     default="result,validations",
#     show_default=True,
# )
# @pass_haproxy_config_svc
# def delete(firewall_server_svc: FirewallAliasFacade, **kwargs):
#     """
#     Delete an server
#     """
#     result = firewall_server_svc.delete_server(kwargs['name'])
#
#     CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
