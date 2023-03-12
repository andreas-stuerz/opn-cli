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
    def TEMPLATE_TYPE_attributes_namevar(self):
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
            name=self._params['name'],
            param_type_name=self._params['param_type_name'],
            opts=self._params['opts'],
            secondary_opts=self._params['secondary_opts'],
            type=self._params['type'],
            required=self._params['required'],
            nargs=self._params['nargs'],
            multiple=self._params['multiple'],
            default=self._params['default'],
            envvar=self._params['envvar'],
            help=self._params['help'],
            prompt=self._params['prompt'],
            is_flag=self._params['is_flag'],
            flag_value=self._params['flag_value'],
            count=self._params['count'],
            hidden=self._params['hidden'],
            click_group=self._click_group,
            click_command=self._click_command,
        ).strip()

    @property
    def _template(self):
        return self.__template

    @_template.setter
    def _template(self, template):
        self.__template = Template(textwrap.dedent(template))



