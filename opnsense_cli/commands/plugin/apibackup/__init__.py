import click


@click.group()
def apibackup(**kwargs):
    """
    Manage api-backup operations (OPNsense version <= 23.7)
    """
