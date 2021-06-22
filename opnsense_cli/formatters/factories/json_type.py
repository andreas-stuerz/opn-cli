from opnsense_cli.formatters.factories.base import TypeFactory
from opnsense_cli.formatters.types.base import JsonType
from opnsense_cli.formatters.types.json_array import JsonArray
from opnsense_cli.formatters.types.json_nested import JsonObjNested


class JsonTypeFactory(TypeFactory):
    def get_type_for_data(self, data) -> JsonType:
        if isinstance(data, list):
            return JsonArray(data)

        if isinstance(data, dict):
            for key, val in data.items():
                if not isinstance(val, dict):
                    data = [data]
                    return JsonArray(data)
            return JsonObjNested(data)

        raise NotImplementedError("Type of JSON is unknown.")
