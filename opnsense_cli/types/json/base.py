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
