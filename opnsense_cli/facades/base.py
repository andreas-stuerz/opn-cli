from abc import ABC


class CommandFacade(ABC):
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

    def _sort_dict_by_string(self, dict, by_column):
        return sorted(dict, key=lambda k: k[by_column])

    def _sort_dict_by_number(self, dict, by_column):
        return sorted(dict, key=lambda k: int(k[by_column]))
