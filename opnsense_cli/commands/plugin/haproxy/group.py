import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats
from opnsense_cli.commands.plugin.haproxy import haproxy
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.haproxy import Settings, Service
from opnsense_cli.facades.commands.plugin.haproxy.group import HaproxyGroupFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_haproxy_group_svc = click.make_pass_decorator(HaproxyGroupFacade)


@haproxy.group()
@pass_api_client
@click.pass_context
def group(ctx, api_client: ApiClient, **kwargs):
    """
    HTTP basic authentication groups.
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = HaproxyGroupFacade(settings_api, service_api)


@group.command()
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
        "uuid,enabled,name,description,Users,add_userlist"
    ),
    show_default=True,
)
@pass_haproxy_group_svc
def list(haproxy_group_svc: HaproxyGroupFacade, **kwargs):
    """
    Show all group
    """
    result = haproxy_group_svc.list_groups()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@group.command()
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
        "enabled,name,description,Users,add_userlist"
    ),
    show_default=True,
)
@pass_haproxy_group_svc
def show(haproxy_group_svc: HaproxyGroupFacade, **kwargs):
    """
    Show details for group
    """
    result = haproxy_group_svc.show_group(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@group.command()
@click.argument('name')
@click.option(
    '--enabled/--no-enabled',
    help=('Enable this group.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--description',
    help=('Description for this group.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--members',
    help=('The comma seperated user uuids of the group.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--add_userlist/--no-add_userlist',
    help=(
        'Usually HAproxy userlists are created automatically in a context sensitive way. "'
        '"This option adds this group as userlist, so that it can be referenced in rules/conditions. "'
        '"All special and non-alphanumeric characters will be removed from the userlist name.'
    ),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
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
@pass_haproxy_group_svc
def create(haproxy_group_svc: HaproxyGroupFacade, **kwargs):
    """
    Create a new group
    """
    json_payload = {
        'group': {
            "enabled": kwargs['enabled'],
            "name": kwargs['name'],
            "description": kwargs['description'],
            "members": kwargs['members'],
            "add_userlist": kwargs['add_userlist'],
        }
    }

    result = haproxy_group_svc.create_group(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@group.command()
@click.argument('uuid')
@click.option(
    '--enabled/--no-enabled',
    help=('Enable this group.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--name',
    help=('Name to identify this group.'),
    show_default=True,
    default=None
)
@click.option(
    '--description',
    help=('Description for this group.'),
    show_default=True,
    default=None
)
@click.option(
    '--members',
    help=('The comma seperated user uuids of the group'),
    show_default=True,
    default=None
)
@click.option(
    '--add_userlist/--no-add_userlist',
    help=(
        'Usually HAproxy userlists are created automatically in a context sensitive way. "'
        '"This option adds this group as userlist, so that it can be referenced in rules/conditions. "'
        '"All special and non-alphanumeric characters will be removed from the userlist name.'
    ),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
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
@pass_haproxy_group_svc
def update(haproxy_group_svc: HaproxyGroupFacade, **kwargs):
    """
    Update a group.
    """
    json_payload = {
        'group': {}
    }
    options = ['enabled', 'name', 'description', 'members', 'add_userlist']
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['group'][option] = kwargs[option.lower()]

    result = haproxy_group_svc.update_group(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@group.command()
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
@pass_haproxy_group_svc
def delete(haproxy_group_svc: HaproxyGroupFacade, **kwargs):
    """
    Delete group
    """
    result = haproxy_group_svc.delete_group(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
