import click
from opnsense_cli.click_addons.command_tree import _build_command_tree, _print_tree


@click.command()
@click.pass_context
def tree(ctx):
    """
    Show the command tree of your CLI
    """
    root_cmd = _build_command_tree(ctx.find_root().command)
    _print_tree(root_cmd)


