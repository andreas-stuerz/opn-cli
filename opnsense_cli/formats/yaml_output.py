import click
import json
import yaml
from opnsense_cli.formats.base import Format


class YamlOutputFormat(Format):
    def echo(self):
        json_type = self.get_json_type()
        filtered_data = json_type.get_filtered_by_columns(self._cols)

        if len(filtered_data) > 1:
            result = self._get_multi(filtered_data)
        else:
            result = self._get_single(filtered_data[0])

        click.echo(yaml.dump(result,  sort_keys=False))

    def _get_single(self, line):
        return dict(zip(self._cols, line))

    def _get_multi(self, lines):
        result = []
        for line in lines:
            result.append(dict(zip(self._cols, line)))
        return result
