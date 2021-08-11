from opnsense_cli.types.json.base import JsonType


class JsonObj(JsonType):
    def get_filtered_by_columns(self, filter_columns):
        filtered_json_data = {column: self._json_data.get(column, "") for column in filter_columns}
        result = [str(json_value) for json_value in filtered_json_data.values()]
        return [result]

    def get_all_columns(self):
        return list(self._json_data.keys())
