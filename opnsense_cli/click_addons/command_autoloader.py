import os
import importlib
import importlib.util


class ClickCommandAutoloader:
    def __init__(self, click_core_group):
        self.loaded_modules = []
        self.loaded_classes = []
        self.subgroups = {}
        self.click_core_group = click_core_group

    def autoload(self, module_name=None, ignore_dirs=None):
        """
        Autoloads all click commands from the specified module.
        Each command group must be in a single subpackage.
        The main click group should be in the __init__.py file.
        Subcommands filenames must match the sub click group.

        e.g. for module name opnsense_cli.commands.core

        opnsense_cli/commands/
        ├── core/
        │ ├── firewall/
        │ │ ├── tests/ (put your tests here)
        │ │ ├── services/ (put your services here)
        │ │ ├── __init__.py (main @click.group firewall)
        │ │ ├── alias.py (subgroup alias with commands from firewall)
        │ │ └── rule.py (subgroup rule with commands from firewall)

        :param module_name: python module name e.g. opnsense_cli.commands.core
        :return: click.core.Group
        """
        if ignore_dirs is None:
            ignore_dirs = ["__pycache__", "tests", "services"]

        spec = importlib.util.find_spec(module_name)
        path = spec.submodule_search_locations[0]

        (root_dir, command_group_dirs, files) = list(os.walk(path))[0]
        command_group_dirs = [directory for directory in command_group_dirs if directory not in ignore_dirs]

        if not command_group_dirs:
            path, file = os.path.split(root_dir)
            command_group_dirs = [file]
            module_path_components = module_name.split(".")
            module_name = ".".join(module_path_components[:-1])

        for command_group_dir in command_group_dirs:
            command_group_files = sorted(list(os.walk(f"{path}/{command_group_dir}"))[0][2])

            for command_group_file in command_group_files:
                if command_group_file == "__init__.py":
                    import_name = f"{module_name}.{command_group_dir}"
                    class_name = command_group_dir
                else:
                    _subname_ = os.path.splitext(command_group_file)[0]
                    import_name = f"{module_name}.{command_group_dir}.{_subname_}"
                    class_name = _subname_

                module = importlib.import_module(import_name)
                click_group = getattr(module, class_name)

                self.loaded_modules.append(module)
                self.loaded_classes.append(click_group)

                if command_group_file == "__init__.py":
                    self.click_core_group.add_command(click_group)
                    self.subgroups[command_group_dir] = click_group

        return self.click_core_group
