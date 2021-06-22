from opnsense_cli.formatters.types.base import JsonType


class JsonObjNested(JsonType):
    """
    Table Output for nested json Objects.
    Example:
    {
        '567f2891c6002': {'description': 'vpn name 1', 'users': []},
        '567f28af0cb4d': {'description': 'vpn name 2', 'users': []}
    }
    """
    def __init__(self, json_data):
        json_data_with_id = self.__extract_id_column(json_data)
        super().__init__(json_data_with_id)

    def __extract_id_column(self, json_data):
        """
        Extract the key of each json row and add it in each json obj with attribute name <ID>
        """
        result = []
        for item in json_data:
            line = {}
            line.update({
                '<ID>': item
            })
            line.update(json_data[item])
            result.append(line)
        return result

    def get_filtered_by_columns(self, filter_columns):
        return super().get_filtered_by_columns(filter_columns)
