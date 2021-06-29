from opnsense_cli.types.json.base import JsonType


class JsonObj(JsonType):
    def get_filtered_by_columns(self, filter_columns):
        filtered_json_data = dict(filter(lambda elem: elem[0] in filter_columns, self._json_data.items()))
        result = [str(json_value) for json_value in filtered_json_data.values()]
        return [result]
