import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats
from opnsense_cli.commands.plugin.haproxy import haproxy
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.haproxy import Settings, Service
from opnsense_cli.facades.commands.plugin.haproxy.user import HaproxyUserFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_haproxy_user_svc = click.make_pass_decorator(HaproxyUserFacade)


@haproxy.group()
@pass_api_client
@click.pass_context
def user(ctx, api_client: ApiClient, **kwargs):
    """
    HTTP basic authentication users.
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = HaproxyUserFacade(settings_api, service_api)


@user.command()
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
        "uuid,enabled,name,description,password"
    ),
    show_default=True,
)
@pass_haproxy_user_svc
def list(haproxy_user_svc: HaproxyUserFacade, **kwargs):
    """
    Show all user
    """
    result = haproxy_user_svc.list_users()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@user.command()
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
        "enabled,name,description,password"
    ),
    show_default=True,
)
@pass_haproxy_user_svc
def show(haproxy_user_svc: HaproxyUserFacade, **kwargs):
    """
    Show details for user
    """
    result = haproxy_user_svc.show_user(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@user.command()
@click.argument('name')
@click.option(
    '--enabled/--no-enabled',
    help=('Enable this user.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--description',
    help=('Description for this user.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--password',
    help=(
        'Both encrypted and unencrypted passwords can be used. Most systems support MD5, SHA-256, SHA-512, and, '
        'of course, the classic DES-based method of encrypting passwords. '
        'NOTE: Avoid using unencrypted passwords that start with a $-sign, because this indicates an encrypted '
        'password and will make it impossible to authenticate.'
    ),
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
@pass_haproxy_user_svc
def create(haproxy_user_svc: HaproxyUserFacade, **kwargs):
    """
    Create a new user
    """
    json_payload = {
        'user': {
            "enabled": kwargs['enabled'],
            "name": kwargs['name'],
            "description": kwargs['description'],
            "password": kwargs['password'],
        }
    }

    result = haproxy_user_svc.create_user(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@user.command()
@click.argument('uuid')
@click.option(
    '--enabled/--no-enabled',
    help=('Enable this user.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--name',
    help=('Name to identify this user.'),
    show_default=True,
    default=None
)
@click.option(
    '--description',
    help=('Description for this user.'),
    show_default=True,
    default=None
)
@click.option(
    '--password',
    help=(
        'Both encrypted and unencrypted passwords can be used. Most systems support MD5, SHA-256, SHA-512, and, '
        'of course, the classic DES-based method of encrypting passwords. '
        'NOTE: Avoid using unencrypted passwords that start with a $-sign, because this indicates an encrypted '
        'password and will make it impossible to authenticate.'
    ),
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
@pass_haproxy_user_svc
def update(haproxy_user_svc: HaproxyUserFacade, **kwargs):
    """
    Update a user.
    """
    json_payload = {
        'user': {}
    }
    options = ['enabled', 'name', 'description', 'password']
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['user'][option] = kwargs[option.lower()]

    result = haproxy_user_svc.update_user(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@user.command()
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
@pass_haproxy_user_svc
def delete(haproxy_user_svc: HaproxyUserFacade, **kwargs):
    """
    Delete user
    """
    result = haproxy_user_svc.delete_user(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
