import click

from api.client import ApiClient
from api.firmware import Firmware

pass_api_client = click.make_pass_decorator(ApiClient)
pass_firmware_svc = click.make_pass_decorator(Firmware)

@click.group()
@pass_api_client
@click.pass_context
def plugin(ctx, api_client: ApiClient, **kwargs):
    ctx.obj = Firmware(api_client)

@plugin.command()
@pass_firmware_svc
def list(firmware_svc : Firmware, **kwargs):
    click.echo(firmware_svc.info()['plugin'])
    #click.echo(firmware_svc.changelog('18.1'))
