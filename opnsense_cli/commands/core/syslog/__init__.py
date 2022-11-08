import click


@click.group()
def syslog(**kwargs):
    """
    Manage syslog
    """
