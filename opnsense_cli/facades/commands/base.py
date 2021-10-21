from abc import ABC
import base64
from jsonpath_ng.ext import parse
from opnsense_cli.exceptions.command import CommandException
from uuid import UUID


class CommandFacade(ABC):
    def __init__(self):
        self._complete_model_data_cache = None

    @property
    def _complete_model_data(self):
        if self._complete_model_data_cache is None:
            self._complete_model_data_cache = self._settings_api.get()

        return self._complete_model_data_cache

    def _api_mutable_model_get(self, complete_model_data, jsonpath_base, resolver_map, sort_by='name'):
        raw_items = self._get_model_data_slice_with_jsonpath(jsonpath_base, complete_model_data)

        items = []

        if not isinstance(raw_items, dict):
            return items

        for uuid, item_raw in raw_items.items():
            item = self._api_mutable_model_get_items_to_json(item_raw)

            item.update({'uuid': uuid})

            for jsonpath_resolve_key, jsonpath in resolver_map.items():
                resolved_items = self._resolve_linked_items_from_uuids_with_jsonpath_template(
                    item[jsonpath_resolve_key],
                    resolver_map[jsonpath_resolve_key],
                    complete_model_data
                )
                item.update(resolved_items)

            items.append(item)

        items = self._sort_dict_by_string(items, sort_by)
        return items

    def _get_model_data_slice_with_jsonpath(self, path, data) -> dict:
        expression = parse(path)
        slice = [match.value for match in expression.find(data)][0]

        return slice

    def _api_mutable_model_get_items_to_json(self, api_response: dict):
        """
        Extract data without default values from opnsense ApiMutableModelControllerBase function getItems.

        See: https://docs.opnsense.org/development/examples/using_grids.html?highlight=searchbase#api-controller
        :return: dict
        """
        result = {}
        for key, val in api_response.items():
            if isinstance(val, dict):
                selected_val = ",".join([
                    choice_key for choice_key, choice_dict in val.items() if choice_dict["selected"] == 1
                ])
            else:
                selected_val = val
            result[key] = selected_val
        return result

    def _resolve_linked_items_from_uuids_with_jsonpath_template(self, item_csv_string, map, data):
        if not isinstance(item_csv_string, str):
            return {
                map['insert_as_key']: ""
            }

        quoted_items = "'{}'".format("','".join(item_csv_string.split(",")))
        evaluated_template = map['template'].format(uuids=quoted_items)
        uuid_expression = parse(evaluated_template)
        resolved_linked_items = [match.value for match in uuid_expression.find(data)]

        return {
            map['insert_as_key']: ",".join(resolved_linked_items)
        }

    def _sort_dict_by_string(self, dict, by_column):
        return sorted(dict, key=lambda k: k[by_column])

    def _sort_dict_by_number(self, dict, by_column):
        return sorted(dict, key=lambda k: int(k[by_column]))

    def _write_base64_string_to_zipfile(self, path, base64_data):
        content = base64.b64decode(base64_data)
        with open(path, 'wb') as zipFile:
            zipFile.write(content)

    def resolve_linked_uuids(self, resolve_map, resolve_items):
        uuids = [item for item in resolve_items.split(",") if self.is_uuid(item)]
        names = [item for item in resolve_items.split(",") if not self.is_uuid(item)]

        resolved_items = self._resolve_uuids_from_linked_items_with_jsonpath_template(
            names,
            resolve_map,
            self._complete_model_data
        )

        resolved_items_merged_with_uuids = list(set(resolved_items + uuids))
        return ",".join(resolved_items_merged_with_uuids)

    def is_uuid(self, val):
        try:
            UUID(str(val))
            return True
        except ValueError:
            return False

    def _resolve_uuids_from_linked_items_with_jsonpath_template(self, search_items: list, map, data):
        json_path_template = map['template'].split('[')[0]

        resolved_uuids = {}
        uuid_expression = parse(json_path_template)
        for match in uuid_expression.find(data):
            for uuid, item in match.value.items():
                if item['name'] in search_items:
                    resolved_uuids[item['name']] = uuid

        unresolved_items = self._get_unresolved_items(search_items, resolved_uuids.keys())
        if unresolved_items:
            raise CommandException(f"Could not find uuid for {json_path_template}: {unresolved_items}")

        return list(resolved_uuids.values())

    def _get_unresolved_items(self, search_items: list, resolved_items: list):
        item_diff = set(search_items) - set(resolved_items)
        return list(item_diff)
