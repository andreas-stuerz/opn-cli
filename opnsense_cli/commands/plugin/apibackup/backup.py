import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, expand_path, available_formats
from opnsense_cli.commands.plugin.apibackup import apibackup
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.apibackup import Backup
from opnsense_cli.facades.commands.plugin.apibackup.backup import ApibackupBackupFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_apibackup_backup_svc = click.make_pass_decorator(ApibackupBackupFacade)


@apibackup.group()
@pass_api_client
@click.pass_context
def backup(ctx, api_client: ApiClient, **kwargs):
    """
    Manage api-backup
    """
    backup_api = Backup(api_client)
    ctx.obj = ApibackupBackupFacade(backup_api)


@backup.command()
@click.option(
    '-p', '--path',
    help='The target path.',
    type=click.Path(dir_okay=False),
    default='./config.xml',
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
@pass_apibackup_backup_svc
def download(apibackup_backup_svc: ApibackupBackupFacade, **kwargs):
    """
    Download config.xml from OPNsense.
    """
    result = apibackup_backup_svc.download_backup(kwargs['path'])
    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
