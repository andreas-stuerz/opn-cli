import click


@click.group()
def haproxy(**kwargs):
    """
    Manage haproxy loadbalancer operations
    """
