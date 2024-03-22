from opnsense_cli.factories import ObjectTypeFromDataFactory
from opnsense_cli.formatters.cli_output.json_types import JsonType, JsonArray, JsonObj, JsonObjNested


class JsonTypeFactory(ObjectTypeFromDataFactory):
    def get_type_for_data(self, data) -> JsonType:
        if isinstance(data, list):
            return JsonArray(data)

        if isinstance(data, dict):
            for key, val in data.items():
                if not isinstance(val, dict):
                    return JsonObj(data)

            return JsonObjNested(data)

        raise NotImplementedError("Type of JSON is unknown.")
