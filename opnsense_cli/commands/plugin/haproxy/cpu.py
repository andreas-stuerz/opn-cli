import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats, tuple_to_csv
from opnsense_cli.commands.plugin.haproxy import haproxy
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.haproxy import Settings, Service
from opnsense_cli.facades.commands.plugin.haproxy.cpu import HaproxyCpuFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_haproxy_cpu_svc = click.make_pass_decorator(HaproxyCpuFacade)


@haproxy.group()
@pass_api_client
@click.pass_context
def cpu(ctx, api_client: ApiClient, **kwargs):
    """
    CPU affinity rules.
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = HaproxyCpuFacade(settings_api, service_api)


@cpu.command()
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
        "uuid,enabled,name,process_id,thread_id,cpu_id"
    ),
    show_default=True,
)
@pass_haproxy_cpu_svc
def list(haproxy_cpu_svc: HaproxyCpuFacade, **kwargs):
    """
    Show all cpu
    """
    result = haproxy_cpu_svc.list_cpus()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@cpu.command()
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
        "uuid,enabled,name,process_id,thread_id,cpu_id"
    ),
    show_default=True,
)
@pass_haproxy_cpu_svc
def show(haproxy_cpu_svc: HaproxyCpuFacade, **kwargs):
    """
    Show details for cpu
    """
    result = haproxy_cpu_svc.show_cpu(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@cpu.command()
@click.argument('name')
@click.option(
    '--enabled/--no-enabled',
    help=('Enable this CPU affinity rule.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--process_id',
    help=('Process ID that should bind to a specific CPU set. Any process IDs above nbproc are ignored.'),
    type=click.Choice(
        [
            'all', 'odd', 'even', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13',
            'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26', 'x27', 'x28',
            'x29', 'x30', 'x31', 'x32', 'x33', 'x34', 'x35', 'x36', 'x37', 'x38', 'x39', 'x40', 'x41', 'x42', 'x43',
            'x44', 'x45', 'x46', 'x47', 'x48', 'x49', 'x50', 'x51', 'x52', 'x53', 'x54', 'x55', 'x56', 'x57', 'x58',
            'x59', 'x60', 'x61', 'x62', 'x63'
        ]
    ),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None,
    required=True,
)
@click.option(
    '--thread_id',
    help=('Thread ID that should bind to a specific CPU set. Any thread IDs above nbthread are ignored.'),
    type=click.Choice(
        [
            'all', 'odd', 'even', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13',
            'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26', 'x27', 'x28',
            'x29', 'x30', 'x31', 'x32', 'x33', 'x34', 'x35', 'x36', 'x37', 'x38', 'x39', 'x40', 'x41', 'x42', 'x43',
            'x44', 'x45', 'x46', 'x47', 'x48', 'x49', 'x50', 'x51', 'x52', 'x53', 'x54', 'x55', 'x56', 'x57', 'x58',
            'x59', 'x60', 'x61', 'x62', 'x63'
        ]
    ),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None,
    required=True,
)
@click.option(
    '--cpu_id',
    help=('Bind the process/thread ID to this CPU.'),
    type=click.Choice(
        [
            'all', 'odd', 'even', 'x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12',
            'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26', 'x27',
            'x28', 'x29', 'x30', 'x31', 'x32', 'x33', 'x34', 'x35', 'x36', 'x37', 'x38', 'x39', 'x40', 'x41', 'x42',
            'x43', 'x44', 'x45', 'x46', 'x47', 'x48', 'x49', 'x50', 'x51', 'x52', 'x53', 'x54', 'x55', 'x56', 'x57',
            'x58', 'x59', 'x60', 'x61', 'x62', 'x63'
        ]
    ),
    multiple=True,
    callback=tuple_to_csv,
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
@pass_haproxy_cpu_svc
def create(haproxy_cpu_svc: HaproxyCpuFacade, **kwargs):
    """
    Create a new cpu
    """
    json_payload = {
        'cpu': {
            "enabled": kwargs['enabled'],
            "name": kwargs['name'],
            "process_id": kwargs['process_id'],
            "thread_id": kwargs['thread_id'],
            "cpu_id": kwargs['cpu_id'],
        }
    }

    result = haproxy_cpu_svc.create_cpu(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@cpu.command()
@click.argument('uuid')
@click.option(
    '--enabled/--no-enabled',
    help=('Enable this CPU affinity rule.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--name',
    help=('Choose a name for this CPU affinity rule.'),
    show_default=True,
    default=None
)
@click.option(
    '--process_id',
    help=('Process ID that should bind to a specific CPU set. Any process IDs above nbproc are ignored.'),
    type=click.Choice(
        [
            'all', 'odd', 'even', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13',
            'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26', 'x27', 'x28',
            'x29', 'x30', 'x31', 'x32', 'x33', 'x34', 'x35', 'x36', 'x37', 'x38', 'x39', 'x40', 'x41', 'x42', 'x43',
            'x44', 'x45', 'x46', 'x47', 'x48', 'x49', 'x50', 'x51', 'x52', 'x53', 'x54', 'x55', 'x56', 'x57', 'x58',
            'x59', 'x60', 'x61', 'x62', 'x63'
        ]
    ),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--thread_id',
    help=('Thread ID that should bind to a specific CPU set. Any thread IDs above nbthread are ignored.'),
    type=click.Choice(
        [
            'all', 'odd', 'even', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13',
            'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26', 'x27', 'x28',
            'x29', 'x30', 'x31', 'x32', 'x33', 'x34', 'x35', 'x36', 'x37', 'x38', 'x39', 'x40', 'x41', 'x42', 'x43',
            'x44', 'x45', 'x46', 'x47', 'x48', 'x49', 'x50', 'x51', 'x52', 'x53', 'x54', 'x55', 'x56', 'x57', 'x58',
            'x59', 'x60', 'x61', 'x62', 'x63'
        ]
    ),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--cpu_id',
    help=('Bind the process/thread ID to this CPU.'),
    type=click.Choice(
        [
            'all', 'odd', 'even', 'x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12',
            'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26', 'x27',
            'x28', 'x29', 'x30', 'x31', 'x32', 'x33', 'x34', 'x35', 'x36', 'x37', 'x38', 'x39', 'x40', 'x41', 'x42',
            'x43', 'x44', 'x45', 'x46', 'x47', 'x48', 'x49', 'x50', 'x51', 'x52', 'x53', 'x54', 'x55', 'x56', 'x57',
            'x58', 'x59', 'x60', 'x61', 'x62', 'x63'
        ]
    ),
    multiple=True,
    callback=tuple_to_csv,
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
@pass_haproxy_cpu_svc
def update(haproxy_cpu_svc: HaproxyCpuFacade, **kwargs):
    """
    Update a cpu.
    """
    json_payload = {
        'cpu': {}
    }
    options = ['enabled', 'name', 'process_id', 'thread_id', 'cpu_id']
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['cpu'][option] = kwargs[option.lower()]

    result = haproxy_cpu_svc.update_cpu(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@cpu.command()
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
@pass_haproxy_cpu_svc
def delete(haproxy_cpu_svc: HaproxyCpuFacade, **kwargs):
    """
    Delete cpu
    """
    result = haproxy_cpu_svc.delete_cpu(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
