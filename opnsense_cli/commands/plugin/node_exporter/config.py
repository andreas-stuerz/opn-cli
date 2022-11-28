import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats, int_as_string
from opnsense_cli.types.click_param_type.int_or_empty import INT_OR_EMPTY
from opnsense_cli.commands.plugin.node_exporter import nodeexporter
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.nodeexporter import General, Service
from opnsense_cli.facades.commands.plugin.nodeexporter.config import NodeexporterConfigFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_nodeexporter_config_svc = click.make_pass_decorator(NodeexporterConfigFacade)


@nodeexporter.group()
@pass_api_client
@click.pass_context
def config(ctx, api_client: ApiClient, **kwargs):
    """
    Manage nodeexporter config
    """
    settings_api = General(api_client)
    service_api = Service(api_client)
    ctx.obj = NodeexporterConfigFacade(settings_api, service_api)


@config.command()
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
        ""
    ),
    show_default=True,
)
@pass_nodeexporter_config_svc
def show(nodeexporter_config_svc: NodeexporterConfigFacade, **kwargs):
    """
    Show configuration
    """
    result = nodeexporter_config_svc.show_config()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@config.command()
@click.option(
    '--enabled/--no-enabled',
    help=('This will activate the node_exporter plugin.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--listenaddress',
    help=('Set node_exporter\'s listen address. By default, node_exporter will listen on 0.0.0.0 (all interfaces).'),
    show_default=True,
    default=None
)
@click.option(
    '--listenport',
    help=('Set node_exporter\'s listen port. By default, node_exporter will listen on port 9100.'),
    show_default=True,
    type=INT_OR_EMPTY,
    callback=int_as_string,
    default=None
)
@click.option(
    '--cpu/--no-cpu',
    help=('Enable the CPU collector.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--exec/--no-exec',
    help=('Enable the EXEC collector.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--filesystem/--no-filesystem',
    help=('Enable the FILESYSTEM collector.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--loadavg/--no-loadavg',
    help=('Enable the LOADAVG collector.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--meminfo/--no-meminfo',
    help=('Enable the MEMINFO collector.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--netdev/--no-netdev',
    help=('Enable the NETDEV collector.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--time/--no-time',
    help=('Enable the TIME collector.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--devstat/--no-devstat',
    help=('Enable the DEVSTAT collector.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--interrupts/--no-interrupts',
    help=('Enable the INTERRUPTS collector.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--ntp/--no-ntp',
    help=('Enable the NTP collector.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--zfs/--no-zfs',
    help=('Enable the ZFS collector.'),
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
@pass_nodeexporter_config_svc
def edit(nodeexporter_config_svc: NodeexporterConfigFacade, **kwargs):
    """
    Edit configuration
    """
    json_payload = {
        'general': {}
    }
    options = [
        'enabled', 'listenaddress', 'listenport', 'cpu', 'exec', 'filesystem', 'loadavg',
        'meminfo', 'netdev', 'time', 'devstat', 'interrupts', 'ntp', 'zfs',
    ]
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['general'][option] = kwargs[option.lower()]

    result = nodeexporter_config_svc.edit_config(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
