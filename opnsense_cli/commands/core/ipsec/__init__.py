import click


@click.group()
def ipsec(**kwargs):
    """
    Manage Ipsec
    """


@ipsec.group()
def tunnel(**kwargs):
    """
    Manage ipsec tunnels
    """
