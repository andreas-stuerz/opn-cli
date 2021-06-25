from opnsense_cli.types.json.base import JsonType


class JsonArray(JsonType):
    def get_filtered_by_columns(self, filter_columns):
        return super().get_filtered_by_columns(filter_columns)
