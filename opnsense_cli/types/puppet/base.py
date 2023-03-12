from abc import ABC, abstractmethod
from string import Template
import textwrap


class PuppetCodeFragment(ABC):
    def __init__(self, params, find_uuid_by_column, click_group, click_command):
        self._params = params
        self._find_uuid_by_column = find_uuid_by_column
        self._click_group = click_group
        self._click_command = click_command

    @property
    @abstractmethod
    def TEMPLATE_PROVIDER_translate_json_object_to_puppet_resource(self):
        """ This property should be implemented. """

    @property
    @abstractmethod
    def TEMPLATE_PROVIDER_translate_puppet_resource_to_command_args(self):
        """ This property should be implemented. """

    @property
    @abstractmethod
    def TEMPLATE_TYPE_example(self):
        """ This property should be implemented. """

    @property
    @abstractmethod
    def TEMPLATE_TYPE_attributes(self):
        """ This property should be implemented. """

    @property
    @abstractmethod
    def TEMPLATE_TYPE_UNIT_TEST_new_resource(self):
        """ This property should be implemented. """

    @property
    @abstractmethod
    def TEMPLATE_PROVIDER_UNIT_TEST_json(self):
        """ This property should be implemented. """

    @property
    @abstractmethod
    def TEMPLATE_PROVIDER_UNIT_TEST_ruby_hash(self):
        """ This property should be implemented. """

    @property
    @abstractmethod
    def TEMPLATE_ACCEPTANCE_TEST_create_item(self):
        """ This property should be implemented. """

    @property
    @abstractmethod
    def TEMPLATE_ACCEPTANCE_TEST_match_item(self):
        """ This property should be implemented. """

    def get_code_fragment(self, template):
        self._template = template
        return self._render_template()

    def _render_template(self):
        return self._template.substitute(
            name=self._params.get('name'),
            param_type_name=self._params.get('param_type_name'),
            opts=self._params.get('opts'),
            secondary_opts=self._params.get('secondary_opts'),
            type=self._params.get('type'),
            required=self._params.get('required'),
            nargs=self._params.get('nargs'),
            multiple=self._params.get('multiple'),
            default=self._params.get('default') if self._params.get('default') else self.get_empty_default(),
            envvar=self._params.get('envvar'),
            help=self._params.get('help', '').replace("'", "\\'"),
            prompt=self._params.get('prompt'),
            is_flag=self._params.get('is_flag'),
            flag_value=self._params.get('flag_value'),
            count=self._params.get('count'),
            hidden=self._params.get('hidden'),
            choices=self._params.get('type', {}).get('choices'),
            click_group=self._click_group,
            click_command=self._click_command,
        ).strip()

    @property
    def _template(self):
        return self.__template

    @_template.setter
    def _template(self, template):
        self.__template = Template(textwrap.dedent(template))

    def get_empty_default(self):
        return ''



