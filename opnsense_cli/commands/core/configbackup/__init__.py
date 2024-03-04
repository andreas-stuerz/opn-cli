import click


@click.group()
def configbackup(**kwargs):
    """
    Manage api-backup operations (OPNsense version >= 24.1)
    """
