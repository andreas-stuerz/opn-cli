import click


@click.group()
def nodeexporter(**kwargs):
    """
    Manage prometheus exporter for hardware and OS metrics.
    """
