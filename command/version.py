import click


@click.group()
def version(**kwargs):
    """
    Show the version
    """
    click.echo("plugin Group")
