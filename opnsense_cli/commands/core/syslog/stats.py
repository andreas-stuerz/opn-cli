import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, available_formats
from opnsense_cli.commands.core.syslog import syslog
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.core.syslog import Service
from opnsense_cli.facades.commands.core.syslog.stats import SyslogStatsFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_syslog_stats_svc = click.make_pass_decorator(SyslogStatsFacade)


@syslog.group()
@pass_api_client
@click.pass_context
def stats(ctx, api_client: ApiClient, **kwargs):
    """
    Show syslog stats
    """
    service_api = Service(api_client)
    ctx.obj = SyslogStatsFacade(service_api)


@stats.command()
@click.option(
    '--search',
    help=('Search for this string'),
    show_default=True,
    default=None,
    required=False,
)
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
            "#,Description,SourceName,SourceId,SourceInstance,State,Type,Number"
    ),
    show_default=True,
)
@pass_syslog_stats_svc
def list(syslog_stats_svc: SyslogStatsFacade, **kwargs):
    """
    Show syslog statistics
    """
    result = syslog_stats_svc.show_stats(kwargs['search'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
