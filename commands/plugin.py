import click

from opnsense_api.client import ApiClient
from opnsense_api.firmware import Firmware

pass_api_client = click.make_pass_decorator(ApiClient)
pass_firmware_svc = click.make_pass_decorator(Firmware)

@click.group()
@pass_api_client
@click.pass_context
def plugin(ctx, api_client: ApiClient, **kwargs):
    ctx.obj = Firmware(api_client)

@plugin.command()
@pass_firmware_svc
def list(firmware_svc, **kwargs):
    print(firmware_svc)
    result = firmware_svc.info()
    click.echo(result)
