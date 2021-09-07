import click

from opnsense_cli.facades.commands.core.firmware import FirmwareFacade
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import formatter_from_formatter_name, available_formats
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.core.firmware import Firmware

pass_api_client = click.make_pass_decorator(ApiClient)
pass_firmware_svc = click.make_pass_decorator(FirmwareFacade)


@click.group()
@click.option(
    '--time-interval', '-t',
    help='Wait x seconds between query for upgrade status.',
    default=1,
    show_default=True,
)
@pass_api_client
@click.pass_context
def plugin(ctx, api_client: ApiClient, **kwargs):
    """
    OPNsense plugins management
    """
    firmware_api = Firmware(api_client)
    ctx.obj = FirmwareFacade(firmware_api, kwargs['time_interval'])


@plugin.command()
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
    default="name,version,comment,installed",
    show_default=True,
)
@pass_firmware_svc
def list(firmware_svc: FirmwareFacade, **kwargs):
    """
    Show all available plugins.
    """
    result = firmware_svc.plugin_list()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@plugin.command()
@click.option(
    '--output', '-o',
    help='Specifies the output format.',
    default="table",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    default="name,version,comment,locked",
    show_default=True,
)
@pass_firmware_svc
def installed(firmware_svc: FirmwareFacade, **kwargs):
    """
    Show installed plugins.
    """
    result = firmware_svc.plugin_installed()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@plugin.command()
@click.argument('plugin_name')
@click.option(
    '--output', '-o',
    help='Specifies the output format.',
    default="table",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    default="details",
    show_default=True,
)
@pass_firmware_svc
def show(firmware_svc: FirmwareFacade, **kwargs):
    """
    Show plugin details.
    """
    result = firmware_svc.plugin_show(kwargs['plugin_name'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@plugin.command()
@click.argument('plugin_name')
@click.option(
    '--output', '-o',
    help='Specifies the output format.',
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
@pass_firmware_svc
def install(firmware_svc: FirmwareFacade, **kwargs):
    """
    Install plugin by name
    """
    result = firmware_svc.plugin_install(kwargs['plugin_name'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@plugin.command()
@click.argument('plugin_name')
@click.option(
    '--output', '-o',
    help='Specifies the output format.',
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
@pass_firmware_svc
def uninstall(firmware_svc: FirmwareFacade, **kwargs):
    """
    Uninstall plugin by name.
    """
    result = firmware_svc.plugin_uninstall(kwargs['plugin_name'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@plugin.command()
@click.argument('plugin_name')
@click.option(
    '--output', '-o',
    help='Specifies the output format.',
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
@pass_firmware_svc
def reinstall(firmware_svc: FirmwareFacade, **kwargs):
    """
    Reinstall plugin by name.
    """
    result = firmware_svc.plugin_reinstall(kwargs['plugin_name'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@plugin.command()
@click.argument('plugin_name')
@click.option(
    '--output', '-o',
    help='Specifies the output format.',
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
@pass_firmware_svc
def lock(firmware_svc: FirmwareFacade, **kwargs):
    """
    Lock plugin.
    """
    result = firmware_svc.plugin_lock(kwargs['plugin_name'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@plugin.command()
@click.argument('plugin_name')
@click.option(
    '--output', '-o',
    help='Specifies the output format.',
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
@pass_firmware_svc
def unlock(firmware_svc: FirmwareFacade, **kwargs):
    """
    Unlock plugin.
    """
    result = firmware_svc.plugin_unlock(kwargs['plugin_name'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
