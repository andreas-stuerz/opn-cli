from abc import ABC, abstractmethod


class JsonType(ABC):
    def __init__(self, json_data: dict):
        self._json_data = json_data

    @abstractmethod
    def get_filtered_by_columns(self, filter_columns: list) -> list:
        result = []

        for item in self._json_data:
            row = [value for name, value in item.items()]
            if filter_columns:
                row = [str(item[column]) for column in filter_columns]
            result.append(row)
        return result

    def get_all_columns(self):
        result = []
        for row in self._json_data:
            result = list(row.keys())
            break
        return result


class JsonArray(JsonType):
    def get_filtered_by_columns(self, filter_columns):
        return super().get_filtered_by_columns(filter_columns)


class JsonObjNested(JsonType):
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
            line.update({"<ID>": item})
            line.update(json_data[item])
            result.append(line)
        return result

    def get_filtered_by_columns(self, filter_columns):
        return super().get_filtered_by_columns(filter_columns)


class JsonObj(JsonType):
    def get_filtered_by_columns(self, filter_columns):
        filtered_json_data = {column: self._json_data.get(column, "") for column in filter_columns}
        result = [str(json_value) for json_value in filtered_json_data.values()]
        return [result]

    def get_all_columns(self):
        return list(self._json_data.keys())
