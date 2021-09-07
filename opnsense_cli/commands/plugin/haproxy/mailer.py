import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, available_formats, tuple_to_csv
from opnsense_cli.commands.plugin.haproxy import haproxy
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.haproxy import Settings, Service
from opnsense_cli.facades.commands.plugin.haproxy.mailer import HaproxyMailerFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_haproxy_mailer_svc = click.make_pass_decorator(HaproxyMailerFacade)


@haproxy.group()
@pass_api_client
@click.pass_context
def mailer(ctx, api_client: ApiClient, **kwargs):
    """
    Email alerts when the state of servers changes.
    """
    settings_api = Settings(api_client)
    service_api = Service(api_client)
    ctx.obj = HaproxyMailerFacade(settings_api, service_api)


@mailer.command()
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
        "uuid,enabled,name,description,mailservers,sender,recipient,loglevel,timeout,hostname"
    ),
    show_default=True,
)
@pass_haproxy_mailer_svc
def list(haproxy_mailer_svc: HaproxyMailerFacade, **kwargs):
    """
    Show all mailer
    """
    result = haproxy_mailer_svc.list_mailers()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@mailer.command()
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
        "enabled,name,description,mailservers,sender,recipient,loglevel,timeout,hostname"
    ),
    show_default=True,
)
@pass_haproxy_mailer_svc
def show(haproxy_mailer_svc: HaproxyMailerFacade, **kwargs):
    """
    Show details for mailer
    """
    result = haproxy_mailer_svc.show_mailer(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@mailer.command()
@click.argument('name')
@click.option(
    '--enabled/--no-enabled',
    help=('Enable this mailer configuration.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
    required=True,
)
@click.option(
    '--description',
    help=('Choose a optional description for this mailer configuration.'),
    show_default=True,
    default=None,
    required=False,
)
@click.option(
    '--mailservers',
    help=('Add mailservers to this mailer configuration, i.e. 192.168.1.1:25. Use TAB key to complete typing.'),
    show_default=True,
    default=None,
    required=True,
)
@click.option(
    '--sender',
    help=('Declare the from email address to be used in both the envelope and header of email alerts.'),
    show_default=True,
    default=None,
    required=True,
)
@click.option(
    '--recipient',
    help=('Declare both the recipient address in the envelope and to address in the header of email alerts.'),
    show_default=True,
    default=None,
    required=True,
)
@click.option(
    '--loglevel',
    help=(
        'Declare the maximum log level of messages for which email alerts will be sent. '
        'This acts as a filter on the sending of email alerts.'
    ),
    type=click.Choice(['emerg', 'alert', 'crit', 'err', 'warning', 'notice', 'info', 'debug']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default='alert',
    required=True,
)
@click.option(
    '--timeout',
    help=('Defines the time (in seconds) available for a mail/connection to be made and send to the mail server.'),
    show_default=True,
    default='30',
    required=True,
)
@click.option(
    '--hostname',
    help=('Declare the to hostname address to be used when communicating with mailers.'),
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
@pass_haproxy_mailer_svc
def create(haproxy_mailer_svc: HaproxyMailerFacade, **kwargs):
    """
    Create a new mailer
    """
    json_payload = {
        'mailer': {
            "enabled": kwargs['enabled'],
            "name": kwargs['name'],
            "description": kwargs['description'],
            "mailservers": kwargs['mailservers'],
            "sender": kwargs['sender'],
            "recipient": kwargs['recipient'],
            "loglevel": kwargs['loglevel'],
            "timeout": kwargs['timeout'],
            "hostname": kwargs['hostname'],
        }
    }

    result = haproxy_mailer_svc.create_mailer(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@mailer.command()
@click.argument('uuid')
@click.option(
    '--enabled/--no-enabled',
    help=('Enable this mailer configuration.'),
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None
)
@click.option(
    '--name',
    help=('Choose a name for this mailer configuration.'),
    show_default=True,
    default=None
)
@click.option(
    '--description',
    help=('Choose a optional description for this mailer configuration.'),
    show_default=True,
    default=None
)
@click.option(
    '--mailservers',
    help=('Add mailservers to this mailer configuration, i.e. 192.168.1.1:25. Use TAB key to complete typing.'),
    show_default=True,
    default=None
)
@click.option(
    '--sender',
    help=('Declare the from email address to be used in both the envelope and header of email alerts.'),
    show_default=True,
    default=None
)
@click.option(
    '--recipient',
    help=('Declare both the recipient address in the envelope and to address in the header of email alerts.'),
    show_default=True,
    default=None
)
@click.option(
    '--loglevel',
    help=(
        'Declare the maximum log level of messages for which email alerts will be sent. '
        'This acts as a filter on the sending of email alerts.'
    ),
    type=click.Choice(['emerg', 'alert', 'crit', 'err', 'warning', 'notice', 'info', 'debug']),
    multiple=False,
    callback=tuple_to_csv,
    show_default=True,
    default=None
)
@click.option(
    '--timeout',
    help=('Defines the time (in seconds) available for a mail/connection to be made and send to the mail server.'),
    show_default=True,
    default=None
)
@click.option(
    '--hostname',
    help=('Declare the to hostname address to be used when communicating with mailers.'),
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
@pass_haproxy_mailer_svc
def update(haproxy_mailer_svc: HaproxyMailerFacade, **kwargs):
    """
    Update a mailer.
    """
    json_payload = {
        'mailer': {}
    }
    options = ['enabled', 'name', 'description', 'mailservers', 'sender', 'recipient', 'loglevel', 'timeout', 'hostname']
    for option in options:
        if kwargs[option.lower()] is not None:
            json_payload['mailer'][option] = kwargs[option.lower()]

    result = haproxy_mailer_svc.update_mailer(kwargs['uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@mailer.command()
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
@pass_haproxy_mailer_svc
def delete(haproxy_mailer_svc: HaproxyMailerFacade, **kwargs):
    """
    Delete mailer
    """
    result = haproxy_mailer_svc.delete_mailer(kwargs['uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
