import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats, int_as_string, tuple_to_csv
from opnsense_cli.commands.plugin.haproxy import haproxy
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.haproxy import Settings, Service
from opnsense_cli.facades.commands.plugin.haproxy.errorfile import HaproxyErrorfileFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_haproxy_errorfile_svc = click.make_pass_decorator(HaproxyErrorfileFacade)


@haproxy.group()
@pass_api_client
@click.pass_context
def errorfile(ctx, api_client: ApiClient, **kwargs):
    """
    Manage haproxy errorfile
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = HaproxyErrorfileFacade(settings_api, service_api)


@errorfile.command()
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
        "uuid,name,description,code,content"
    ),
    show_default=True,
)
@pass_haproxy_errorfile_svc
def list(haproxy_errorfile_svc: HaproxyErrorfileFacade, **kwargs):
    """
    Show all errorfile
    """
    result = haproxy_errorfile_svc.list_errorfiles()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@errorfile.command()
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
        "name,description,code,content"
    ),
    show_default=True,
)
@pass_haproxy_errorfile_svc
def show(haproxy_errorfile_svc: HaproxyErrorfileFacade, **kwargs):
    """
    Show details for errorfile
    """
    result = haproxy_errorfile_svc.show_errorfile(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@errorfile.command()
@click.argument('name')
@click.option(
    '--description',
    help=('Description for this error message.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--code',
    help=(
        'The HTTP status code. NOTE: It is important to understand that error messages are NOT meant to '
        'rewrite errors returned by the server, but errors detected and returned by HAProxy. '
        'This is why the list of supported errors is limited to a small set.'
    ),
    type=click.Choice(['x200', 'x400', 'x403', 'x405', 'x408', 'x429', 'x500', 'x502', 'x503', 'x504']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='503',
    required=True,
)
@click.option(
    '--content',
    help=(
        'Paste the content of your error messages here. The message must represent the full HTTP response and '
        'include required HTTP headers. '
        'It should not exceed the configured buffer size, which generally is 8 or 16 kB.'
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
@pass_haproxy_errorfile_svc
def create(haproxy_errorfile_svc: HaproxyErrorfileFacade, **kwargs):
    """
    Create a new errorfile
    """
    json_payload = {
        'errorfile': {
            "name": kwargs['name'],
            "description": kwargs['description'],
            "code": kwargs['code'],
            "content": kwargs['content'],
            
        }
    }

    result = haproxy_errorfile_svc.create_errorfile(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@errorfile.command()
@click.argument('uuid')
@click.option(
    '--name',
    help=('Name to identify this error message.'),
    show_default=True,
    default=None
)
@click.option(
    '--description',
    help=('Description for this error message.'),
    show_default=True,
    default=None
)
@click.option(
    '--code',
    help=(
        'The HTTP status code. NOTE: It is important to understand that error messages are NOT meant to '
        'rewrite errors returned by the server, but errors detected and returned by HAProxy. '
        'This is why the list of supported errors is limited to a small set.'
    ),
    type=click.Choice(['x200', 'x400', 'x403', 'x405', 'x408', 'x429', 'x500', 'x502', 'x503', 'x504']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--content',
    help=(
        'Paste the content of your error messages here. The message must represent the full HTTP response and '
        'include required HTTP headers. '
        'It should not exceed the configured buffer size, which generally is 8 or 16 kB.'
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
@pass_haproxy_errorfile_svc
def update(haproxy_errorfile_svc: HaproxyErrorfileFacade, **kwargs):
    """
    Update a errorfile.
    """
    json_payload = {
        'errorfile': {}
    }
    options = ['name', 'description', 'code', 'content']
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['errorfile'][option] = kwargs[option.lower()]

    result = haproxy_errorfile_svc.update_errorfile(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@errorfile.command()
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
@pass_haproxy_errorfile_svc
def delete(haproxy_errorfile_svc: HaproxyErrorfileFacade, **kwargs):
    """
    Delete errorfile
    """
    result = haproxy_errorfile_svc.delete_errorfile(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
