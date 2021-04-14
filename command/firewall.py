import click

@click.group()
def firewall(**kwargs):
    click.echo("plugin Group")

@firewall.command()
def list(**kwargs):
    click.echo("Subcommand for firewall")
