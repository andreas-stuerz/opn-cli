import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats, tuple_to_csv
from opnsense_cli.commands.core.syslog import syslog
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.core.syslog import Settings, Service
from opnsense_cli.facades.commands.core.syslog.destination import SyslogDestinationFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_syslog_destination_svc = click.make_pass_decorator(SyslogDestinationFacade)


@syslog.group()
@pass_api_client
@click.pass_context
def destination(ctx, api_client: ApiClient, **kwargs):
    """
    Manage syslog destination
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = SyslogDestinationFacade(settings_api, service_api)


@destination.command()
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
        "uuid,enabled,transport,program,level,facility,hostname,certificate,port,rfc5424,description"
    ),
    show_default=True,
)
@pass_syslog_destination_svc
def list(syslog_destination_svc: SyslogDestinationFacade, **kwargs):
    """
    Show all destination
    """
    result = syslog_destination_svc.list_destinations()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@destination.command()
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
        "enabled,transport,program,level,facility,hostname,certificate,port,rfc5424,description"
    ),
    show_default=True,
)
@pass_syslog_destination_svc
def show(syslog_destination_svc: SyslogDestinationFacade, **kwargs):
    """
    Show details for destination
    """
    result = syslog_destination_svc.show_destination(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@destination.command()
@click.option(
    '--enabled/--no-enabled',
    help=('Set this option to enable this destination.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--transport',
    help=('Transport protocol'),
    type=click.Choice(['udp4', 'tcp4', 'udp6', 'tcp6', 'tls4', 'tls6']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='udp4',
    required=True,
)
@click.option(
    '--program',
    help=('Choose which applications should be forwarded to the specified target, omit to select all.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--level',
    help=('Choose which levels to include, omit to select all.'),
    type=click.Choice(['', 'debug', 'info', 'notice', 'warn', 'err', 'crit', 'alert', 'emerg']),
    multiple=True,
    callback=tuple_to_csv,
    show_default=True,
    default=['info', 'notice', 'warn', 'err', 'crit', 'alert', 'emerg'],
    required=False,
)
@click.option(
    '--facility',
    help=('Choose which facilities to include, omit to select all.'),
    type=click.Choice(
        [
            '', 'kern', 'user', 'mail', 'daemon', 'auth', 'syslog', 'lpr', 'news', 'uucp', 'cron', 'authpriv', 'ftp', 'ntp',
            'security', 'console', 'local0', 'local1', 'local2', 'local3', 'local4', 'local5', 'local6', 'local7'
        ]
    ),
    multiple=True,
    callback=tuple_to_csv,
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--hostname',
    help=('The hostname or ip address of the syslog destination.'),
    show_default=True,
    default=None,
    required=True,
)
@click.option(
    '--certificate',
    help=('''
        Transport certificate to use, please make sure to check the general system log when experiencing issues.
        Error messages can be a bit cryptic from time to time, in which case
        "https://support.oneidentity.com/kb/263658/common-issues-of-tls-encrypted-message-transfer this is a good
        resource for tracking common issues.
    '''),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--port',
    help=('The port of the syslog destination.'),
    show_default=True,
    default='514',
    required=True,
)
@click.option(
    '--rfc5424/--no-rfc5424',
    help=('Use rfc5424 formated messages for this destination.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--description',
    help=('You may enter a description here for your reference.'),
    show_default=True,
    default=None,
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
@pass_syslog_destination_svc
def create(syslog_destination_svc: SyslogDestinationFacade, **kwargs):
    """
    Create a new destination
    """
    json_payload = {
        'destination': {
            "enabled": kwargs['enabled'],
            "transport": kwargs['transport'],
            "program": kwargs['program'],
            "level": kwargs['level'],
            "facility": kwargs['facility'],
            "hostname": kwargs['hostname'],
            "certificate": kwargs['certificate'],
            "port": kwargs['port'],
            "rfc5424": kwargs['rfc5424'],
            "description": kwargs['description'],
        }
    }

    result = syslog_destination_svc.create_destination(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@destination.command()
@click.argument('uuid')
@click.option(
    '--enabled/--no-enabled',
    help=('Set this option to enable this destination.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--transport',
    help=('Transport protocol'),
    type=click.Choice(['udp4', 'tcp4', 'udp6', 'tcp6', 'tls4', 'tls6']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--program',
    help=('Choose which applications should be forwarded to the specified target, omit to select all.'),
    show_default=True,
    default=None
)
@click.option(
    '--level',
    help=('Choose which levels to include, omit to select all.'),
    type=click.Choice(['', 'debug', 'info', 'notice', 'warn', 'err', 'crit', 'alert', 'emerg']),
    multiple=True,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--facility',
    help=('Choose which facilities to include, omit to select all.'),
    type=click.Choice(
        [
            '', 'kern', 'user', 'mail', 'daemon', 'auth', 'syslog', 'lpr', 'news', 'uucp', 'cron', 'authpriv', 'ftp', 'ntp',
            'security', 'console', 'local0', 'local1', 'local2', 'local3', 'local4', 'local5', 'local6', 'local7'
        ]
    ),
    multiple=True,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--hostname',
    help=('The hostname or ip address of the syslog destination.'),
    show_default=True,
    default=None
)
@click.option(
    '--certificate',
    help=('''
        Transport certificate to use, please make sure to check the general system log when experiencing issues.
        Error messages can be a bit cryptic from time to time, in which case
        https://support.oneidentity.com/kb/263658/common-issues-of-tls-encrypted-message-transfer this is a good
        resource for tracking common issues.
    '''),
    show_default=True,
    default=None
)
@click.option(
    '--port',
    help=('The port of the syslog destination.'),
    show_default=True,
    default=None
)
@click.option(
    '--rfc5424/--no-rfc5424',
    help=('Use rfc5424 formated messages for this destination.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--description',
    help=('You may enter a description here for your reference (not parsed).'),
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
@pass_syslog_destination_svc
def update(syslog_destination_svc: SyslogDestinationFacade, **kwargs):
    """
    Update a destination.
    """
    json_payload = {
        'destination': {}
    }
    options = [
        'enabled', 'transport', 'program', 'level', 'facility', 'hostname', 'certificate', 'port', 'rfc5424', 'description'
    ]
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['destination'][option] = kwargs[option.lower()]

    result = syslog_destination_svc.update_destination(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@destination.command()
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
@pass_syslog_destination_svc
def delete(syslog_destination_svc: SyslogDestinationFacade, **kwargs):
    """
    Delete destination
    """
    result = syslog_destination_svc.delete_destination(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
