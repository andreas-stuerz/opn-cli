import unittest
from click.testing import CliRunner
from opnsense_cli.commands.tree import tree
import click
import textwrap


class TestTreeCommands(unittest.TestCase):
    def test_tree(self):
        @click.group(name="root")
        def root():
            pass

        @root.command(name="command-one")
        def command_one():
            pass

        @root.command(name="command-two")
        def command_two():
            pass

        @click.group(name="sub_level1")
        def sub_level1():
            pass

        @click.group(name="sub_level2")
        def sub_level2():
            pass

        root.add_command(tree)

        root.add_command(sub_level1)
        sub_level1.add_command(command_one)
        sub_level1.add_command(command_two)

        sub_level1.add_command(sub_level2)
        sub_level2.add_command(command_one)
        sub_level2.add_command(command_two)

        runner = CliRunner()
        result = runner.invoke(root, ["tree"])

        tree_output = textwrap.dedent(
            """\
        root
        ├── command-one
        ├── command-two
        ├── sub_level1
        │   ├── command-one
        │   ├── command-two
        │   └── sub_level2
        │       ├── command-one
        │       └── command-two
        └── tree
        """
        )

        self.assertEqual(tree_output, result.output)
