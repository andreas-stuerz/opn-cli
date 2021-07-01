from opnsense_cli.factories.base import ObjectTypeFromDataFactory
from opnsense_cli.types.json.base import JsonType
from opnsense_cli.types.json.json_obj import JsonObj
from opnsense_cli.types.json.json_array import JsonArray
from opnsense_cli.types.json.json_nested import JsonObjNested


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
