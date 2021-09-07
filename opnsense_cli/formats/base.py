from abc import ABC, abstractmethod
from opnsense_cli.factories.json_type import JsonTypeFactory


class Format(ABC):
    def __init__(self, json_data: dict, cols: list, json_type_factory=JsonTypeFactory()):
        self._json_data = json_data
        self._json_type_factory = json_type_factory
        self._cols = self.get_all_cols() if cols == [''] else cols

    def get_all_cols(self):
        json_type = self.get_json_type()
        return json_type.get_all_columns()

    def get_json_type(self):
        return self._json_type_factory.get_type_for_data(self._json_data)

    def get_filtered_data_by_columns(self):
        json_type = self.get_json_type()
        filtered_data = json_type.get_filtered_by_columns(self._cols)

        if len(filtered_data) > 1:
            return self._get_filtered_data_for_list(filtered_data)

        return self._get_filtered_data_for_obj(filtered_data)

    def _get_filtered_data_for_obj(self, line: list):
        if not line:
            return {}
        return dict(zip(self._cols, line[0]))

    def _get_filtered_data_for_list(self, lines: list):
        result = []
        for line in lines:
            result.append(dict(zip(self._cols, line)))
        return result

    @abstractmethod
    def echo(self):
        """ This method should be implemented. """
