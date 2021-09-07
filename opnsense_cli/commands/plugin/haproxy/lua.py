import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats
from opnsense_cli.commands.plugin.haproxy import haproxy
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.haproxy import Settings, Service
from opnsense_cli.facades.commands.plugin.haproxy.lua import HaproxyLuaFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_haproxy_lua_svc = click.make_pass_decorator(HaproxyLuaFacade)


@haproxy.group()
@pass_api_client
@click.pass_context
def lua(ctx, api_client: ApiClient, **kwargs):
    """
    Lua code/scripts to extend HAProxy's functionality.
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = HaproxyLuaFacade(settings_api, service_api)


@lua.command()
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
        "uuid,enabled,name,description,content"
    ),
    show_default=True,
)
@pass_haproxy_lua_svc
def list(haproxy_lua_svc: HaproxyLuaFacade, **kwargs):
    """
    Show all lua
    """
    result = haproxy_lua_svc.list_luas()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@lua.command()
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
        "enabled,name,description,content"
    ),
    show_default=True,
)
@pass_haproxy_lua_svc
def show(haproxy_lua_svc: HaproxyLuaFacade, **kwargs):
    """
    Show details for lua
    """
    result = haproxy_lua_svc.show_lua(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@lua.command()
@click.argument('name')
@click.option(
    '--enabled/--no-enabled',
    help=('Enable this Lua script.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--description',
    help=('Description for this Lua script.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--content',
    help=('Paste the content of your Lua script here.'),
    show_default=True,
    default=None,
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
    default="result,validations",
    show_default=True,
)
@pass_haproxy_lua_svc
def create(haproxy_lua_svc: HaproxyLuaFacade, **kwargs):
    """
    Create a new lua
    """
    json_payload = {
        'lua': {
            "enabled": kwargs['enabled'],
            "name": kwargs['name'],
            "description": kwargs['description'],
            "content": kwargs['content'],
        }
    }

    result = haproxy_lua_svc.create_lua(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@lua.command()
@click.argument('uuid')
@click.option(
    '--enabled/--no-enabled',
    help=('Enable this Lua script.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--name',
    help=('Name to identify this Lua script.'),
    show_default=True,
    default=None
)
@click.option(
    '--description',
    help=('Description for this Lua script.'),
    show_default=True,
    default=None
)
@click.option(
    '--content',
    help=('Paste the content of your Lua script here.'),
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
@pass_haproxy_lua_svc
def update(haproxy_lua_svc: HaproxyLuaFacade, **kwargs):
    """
    Update a lua.
    """
    json_payload = {
        'lua': {}
    }
    options = ['enabled', 'name', 'description', 'content']
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['lua'][option] = kwargs[option.lower()]

    result = haproxy_lua_svc.update_lua(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@lua.command()
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
@pass_haproxy_lua_svc
def delete(haproxy_lua_svc: HaproxyLuaFacade, **kwargs):
    """
    Delete lua
    """
    result = haproxy_lua_svc.delete_lua(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
