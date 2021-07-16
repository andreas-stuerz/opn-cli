import click
import yaml
from opnsense_cli.formats.base import Format


class YamlOutputFormat(Format):
    def echo(self):
        json_type = self.get_json_type()
        filtered_data = json_type.get_filtered_by_columns(self._cols)

        yaml_output = self._get_yaml_from_filtered_data(filtered_data)

        click.echo(yaml_output)

    def _get_yaml_from_filtered_data(self, filtered_data: list):
        if len(filtered_data) > 1:
            result = self._get_for_multi_items(filtered_data)
        else:
            result = self._get_for_single_item(filtered_data)

        result = yaml.dump(result, sort_keys=False)
        return result

    def _get_for_single_item(self, line: list):
        if not line:
            return {}
        return dict(zip(self._cols, line[0]))

    def _get_for_multi_items(self, lines: list):
        result = []
        for line in lines:
            result.append(dict(zip(self._cols, line)))
        return result
