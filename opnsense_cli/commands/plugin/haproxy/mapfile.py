import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, available_formats
from opnsense_cli.commands.plugin.haproxy import haproxy
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.haproxy import Settings, Service
from opnsense_cli.facades.commands.plugin.haproxy.mapfile import HaproxyMapfileFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_haproxy_mapfile_svc = click.make_pass_decorator(HaproxyMapfileFacade)


@haproxy.group()
@pass_api_client
@click.pass_context
def mapfile(ctx, api_client: ApiClient, **kwargs):
    """
    Map a large number of domains to backend pools.

    A map allows to map a data in input to an other one on output. For example, this makes it possible to map a large
    number of domains to backend pools without using the GUI. Map files need to be used in Rules, otherwise
    they are ignored.
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = HaproxyMapfileFacade(settings_api, service_api)


@mapfile.command()
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
        "uuid,name,description,content"
    ),
    show_default=True,
)
@pass_haproxy_mapfile_svc
def list(haproxy_mapfile_svc: HaproxyMapfileFacade, **kwargs):
    """
    Show all mapfile
    """
    result = haproxy_mapfile_svc.list_mapfiles()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@mapfile.command()
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
        "name,description,content"
    ),
    show_default=True,
)
@pass_haproxy_mapfile_svc
def show(haproxy_mapfile_svc: HaproxyMapfileFacade, **kwargs):
    """
    Show details for mapfile
    """
    result = haproxy_mapfile_svc.show_mapfile(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@mapfile.command()
@click.argument('name')
@click.option(
    '--description',
    help=('Description for this map file.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--content',
    help=('Paste the content of your map file here.'),
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
@pass_haproxy_mapfile_svc
def create(haproxy_mapfile_svc: HaproxyMapfileFacade, **kwargs):
    """
    Create a new mapfile
    """
    json_payload = {
        'mapfile': {
            "name": kwargs['name'],
            "description": kwargs['description'],
            "content": kwargs['content'],
        }
    }

    result = haproxy_mapfile_svc.create_mapfile(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@mapfile.command()
@click.argument('uuid')
@click.option(
    '--name',
    help=('Name to identify this map file.'),
    show_default=True,
    default=None
)
@click.option(
    '--description',
    help=('Description for this map file.'),
    show_default=True,
    default=None
)
@click.option(
    '--content',
    help=('Paste the content of your map file here.'),
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
@pass_haproxy_mapfile_svc
def update(haproxy_mapfile_svc: HaproxyMapfileFacade, **kwargs):
    """
    Update a mapfile.
    """
    json_payload = {
        'mapfile': {}
    }
    options = ['name', 'description', 'content']
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['mapfile'][option] = kwargs[option.lower()]

    result = haproxy_mapfile_svc.update_mapfile(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@mapfile.command()
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
@pass_haproxy_mapfile_svc
def delete(haproxy_mapfile_svc: HaproxyMapfileFacade, **kwargs):
    """
    Delete mapfile
    """
    result = haproxy_mapfile_svc.delete_mapfile(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
