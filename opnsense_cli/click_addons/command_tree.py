import click


class _CommandWrapper(object):
    def __init__(self, command=None, children=None):
        self.command = command
        self.children = []

    @property
    def name(self):
        return self.command.name


def _build_command_tree(click_command):
    wrapper = _CommandWrapper(click_command)

    if isinstance(click_command, click.core.Group):
        for _, cmd in click_command.commands.items():
            if not getattr(cmd, "hidden", False):
                wrapper.children.append(_build_command_tree(cmd))

    return wrapper


def _print_tree(command, depth=0, is_last_item=False, is_last_parent=False):
    if depth == 0:
        prefix = ""
        tree_item = ""
    else:
        prefix = "   " if is_last_parent else "│   "
        tree_item = "└── " if is_last_item else "├── "

    root_line = "│ " if is_last_parent else ""

    line = root_line + prefix * (depth - 1) + tree_item + command.name

    click.echo(line)

    for i, child in enumerate(sorted(command.children, key=lambda x: x.name)):
        _print_tree(child, depth=(depth + 1), is_last_item=(i == (len(command.children) - 1)), is_last_parent=is_last_item)
