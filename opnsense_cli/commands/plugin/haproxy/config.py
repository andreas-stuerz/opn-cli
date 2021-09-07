import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, expand_path, available_formats
from opnsense_cli.commands.plugin.haproxy import haproxy
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.haproxy import Settings, Export, Service
from opnsense_cli.facades.commands.plugin.haproxy.config import HaproxyConfigFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_haproxy_config_svc = click.make_pass_decorator(HaproxyConfigFacade)


@haproxy.group()
@pass_api_client
@click.pass_context
def config(ctx, api_client: ApiClient, **kwargs):
    """
    Debug haproxy configuration.
    """
    settings_api = Settings(api_client)
    export_api = Export(api_client)
    service_api = Service(api_client)
    ctx.obj = HaproxyConfigFacade(settings_api, export_api, service_api)


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
    default="result",
    show_default=True,
)
@pass_haproxy_config_svc
def test(haproxy_server_svc: HaproxyConfigFacade, **kwargs):
    """
    Test current haproxy staging config
    """
    result = haproxy_server_svc.test_config()

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
def apply(haproxy_server_svc: HaproxyConfigFacade, **kwargs):
    """
    Test and apply the haproxy configuration
    """
    result = haproxy_server_svc.apply_config()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@config.command()
@click.option(
    '-p', '--path',
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
