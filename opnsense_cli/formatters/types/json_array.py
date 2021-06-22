from opnsense_cli.formatters.types.base import JsonType


class JsonArray(JsonType):
    """
    Transform array of json objects
    Example:
    [
        {"name": "obj1"},
        {"name", "obj2"}
    ]
    """
    def get_filtered_by_columns(self, filter_columns):
        return super().get_filtered_by_columns(filter_columns)
