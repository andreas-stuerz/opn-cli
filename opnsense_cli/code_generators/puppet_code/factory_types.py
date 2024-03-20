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
        """This property should be implemented."""

    @property
    @abstractmethod
    def TEMPLATE_PROVIDER_translate_puppet_resource_to_command_args(self):
        """This property should be implemented."""

    @property
    @abstractmethod
    def TEMPLATE_TYPE_example(self):
        """This property should be implemented."""

    @property
    @abstractmethod
    def TEMPLATE_TYPE_attributes(self):
        """This property should be implemented."""

    @property
    @abstractmethod
    def TEMPLATE_TYPE_UNIT_TEST_new_resource(self):
        """This property should be implemented."""

    @property
    @abstractmethod
    def TEMPLATE_PROVIDER_UNIT_TEST_json(self):
        """This property should be implemented."""

    @property
    @abstractmethod
    def TEMPLATE_PROVIDER_UNIT_TEST_ruby_hash(self):
        """This property should be implemented."""

    @property
    @abstractmethod
    def TEMPLATE_ACCEPTANCE_TEST_create_item(self):
        """This property should be implemented."""

    @property
    @abstractmethod
    def TEMPLATE_ACCEPTANCE_TEST_match_item(self):
        """This property should be implemented."""

    def get_code_fragment(self, template):
        self._template = template
        return self._render_template()

    def _render_template(self):
        return self._template.substitute(
            name=self._params.get("name"),
            param_type_name=self._params.get("param_type_name"),
            opts=self._params.get("opts"),
            secondary_opts=self._params.get("secondary_opts"),
            type=self._params.get("type"),
            required=self._params.get("required"),
            nargs=self._params.get("nargs"),
            multiple=self._params.get("multiple"),
            default=self._params.get("default") if self._params.get("default") else self.get_empty_default(),
            envvar=self._params.get("envvar"),
            help=self._params.get("help", "").replace("'", "\\'"),
            prompt=self._params.get("prompt"),
            is_flag=self._params.get("is_flag"),
            flag_value=self._params.get("flag_value"),
            count=self._params.get("count"),
            hidden=self._params.get("hidden"),
            choices=self._params.get("type", {}).get("choices"),
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
        return ""


class PuppetBoolean(PuppetCodeFragment):
    TEMPLATE_PROVIDER_translate_json_object_to_puppet_resource = """
    ${name}: bool_from_value(json_object['${name}']),
    """

    TEMPLATE_PROVIDER_translate_puppet_resource_to_command_args = """
    args.push('--${name}') if bool_from_value(puppet_resource[:${name}]) == true
            args.push('--no-${name}') if bool_from_value(puppet_resource[:${name}]) == false
    """

    TEMPLATE_TYPE_example = """
    ${name} => TODO,
    """

    TEMPLATE_TYPE_attributes = """
    ${name}: {
          type: 'Boolean',
          desc: '${help}',
        },
    """

    TEMPLATE_TYPE_UNIT_TEST_new_resource = """
    ${name}: true,
    """

    TEMPLATE_TYPE_UNIT_TEST_accepts_parameter = """
    it 'accepts ${name}' do
          ${click_group}_${click_command}[:${name}] = false
          expect(${click_group}_${click_command}[:${name}]).to eq(:false)
        end
    """

    TEMPLATE_PROVIDER_UNIT_TEST_json = """
    "${name}": '1',
    """

    TEMPLATE_PROVIDER_UNIT_TEST_ruby_hash = """
    ${name}: true,
    """

    TEMPLATE_ACCEPTANCE_TEST_create_item = """
    ${name} => false,
    """

    TEMPLATE_ACCEPTANCE_TEST_match_item = """
    expect(r.stdout).to match %r{${name}: '0'}
    """

class PuppetChoice(PuppetCodeFragment):
    TEMPLATE_PROVIDER_translate_json_object_to_puppet_resource = """
    ${name}: json_object['${name}'],
    """

    TEMPLATE_PROVIDER_translate_puppet_resource_to_command_args = """
    args.push('--${name}', puppet_resource[:${name}])
    """

    TEMPLATE_TYPE_example = """
    ${name} => 'TODO',
    """

    TEMPLATE_TYPE_attributes = """
    ${name}: {
          type: "Enum${choices}",
          desc: '${help}',
        },
    """

    TEMPLATE_TYPE_UNIT_TEST_new_resource = """
    ${name}: 'TODO',
    """

    TEMPLATE_TYPE_UNIT_TEST_accepts_parameter = """
    it 'accepts ${name}' do
          ${click_group}_${click_command}[:${name}] = 'a valid TODO choice'
          expect(${click_group}_${click_command}[:${name}]).to eq('a valid TODO choice')
        end
    """

    TEMPLATE_PROVIDER_UNIT_TEST_json = """
    "${name}": 'TODO',
    """

    TEMPLATE_PROVIDER_UNIT_TEST_ruby_hash = """
    ${name}: 'TODO',
    """

    TEMPLATE_ACCEPTANCE_TEST_create_item = """
    ${name} => 'TODO',
    """

    TEMPLATE_ACCEPTANCE_TEST_match_item = """
    expect(r.stdout).to match %r{${name}: 'TODO'}
    """

class PuppetChoiceMultiple(PuppetCodeFragment):
    TEMPLATE_PROVIDER_translate_json_object_to_puppet_resource = """
    ${name}: array_from_value(json_object['${name}']),
    """

    TEMPLATE_PROVIDER_translate_puppet_resource_to_command_args = """
    puppet_resource[:${name}].each do |opt|
              args.push('--${name}', opt)
            end
    """

    TEMPLATE_TYPE_example = """
    ${name} => [],
    """

    TEMPLATE_TYPE_attributes = """
    ${name}: {
          type: "Array[
            Enum${choices}
          ]",
          desc: '${help}',
        },
    """

    TEMPLATE_TYPE_UNIT_TEST_new_resource = """
    ${name}: 'TODO',
    """

    TEMPLATE_TYPE_UNIT_TEST_accepts_parameter = """
    it 'accepts ${name}' do
          ${click_group}_${click_command}[:${name}] = ['valid_TODO_choice', 'another_valid_TODO_choice']
          expect(${click_group}_${click_command}[:${name}]).to eq(['valid_TODO_choice', 'another_valid_TODO_choice'])
        end
    """

    TEMPLATE_PROVIDER_UNIT_TEST_json = """
    "${name}": 'TODO',
    """

    TEMPLATE_PROVIDER_UNIT_TEST_ruby_hash = """
    ${name}: 'TODO',
    """

    TEMPLATE_ACCEPTANCE_TEST_create_item = """
    ${name} => 'TODO',
    """

    TEMPLATE_ACCEPTANCE_TEST_match_item = """
    expect(r.stdout).to match %r{${name}: 'TODO'}
    """

class PuppetCsv(PuppetCodeFragment):
    TEMPLATE_PROVIDER_translate_json_object_to_puppet_resource = """
    ${name}: array_from_value(json_object['${name}']),
    """

    TEMPLATE_PROVIDER_translate_puppet_resource_to_command_args = """
    args.push('--${name}', puppet_resource[:${name}].join(','))
    """

    TEMPLATE_TYPE_example = """
    ${name} => [],
    """

    TEMPLATE_TYPE_attributes = """
    ${name}: {
          type: "Array[String]",
          desc: '${help}',
          default: []
        },
    """

    TEMPLATE_TYPE_UNIT_TEST_new_resource = """
    ${name}: [],
    """

    TEMPLATE_TYPE_UNIT_TEST_accepts_parameter = """
    it 'accepts ${name}' do
          ${click_group}_${click_command}[:${name}] = ['valid item1', 'valid item2']
          expect(${click_group}_${click_command}[:${name}]).to eq(['valid item1', 'valid item2'])
        end
    """

    TEMPLATE_PROVIDER_UNIT_TEST_json = """
    "${name}": 'TODO_CSV',
    """

    TEMPLATE_PROVIDER_UNIT_TEST_ruby_hash = """
    ${name}: ['TODO_CSV'],
    """

    TEMPLATE_ACCEPTANCE_TEST_create_item = """
    ${name} => [],
    """

    TEMPLATE_ACCEPTANCE_TEST_match_item = """
    expect(r.stdout).to match %r{${name}: '\\[\\]'}
    """

class PuppetInteger(PuppetCodeFragment):
    TEMPLATE_PROVIDER_translate_json_object_to_puppet_resource = """
    ${name}: json_object['${name}'],
    """

    TEMPLATE_PROVIDER_translate_puppet_resource_to_command_args = """
    args.push('--${name}', puppet_resource[:${name}])
    """

    TEMPLATE_TYPE_example = """
    ${name} => 'TODO',
    """

    TEMPLATE_TYPE_attributes = """
    ${name}: {
          type: 'String',
          desc: '${help}',
        },
    """

    TEMPLATE_TYPE_attributes_namevar = """
    ${name}: {
          type: 'String',
          desc: '${help}',
          behaviour: :namevar,
        },
    """

    TEMPLATE_TYPE_UNIT_TEST_new_resource = """
    ${name}: 'TODO',
    """

    TEMPLATE_TYPE_UNIT_TEST_accepts_parameter = """
    it 'accepts ${name}' do
          ${click_group}_${click_command}[:${name}] = 'a todo integer'
          expect(${click_group}_${click_command}[:${name}]).to eq('a todo integer')
        end
    """

    TEMPLATE_PROVIDER_UNIT_TEST_json = """
    "${name}": 'TODO',
    """

    TEMPLATE_PROVIDER_UNIT_TEST_ruby_hash = """
    ${name}: 'TODO',
    """

    TEMPLATE_ACCEPTANCE_TEST_create_item = """
    ${name} => 'TODO',
    """

    TEMPLATE_ACCEPTANCE_TEST_match_item = """
    expect(r.stdout).to match %r{${name}: 'TODO'}
    """

class PuppetString(PuppetCodeFragment):
    TEMPLATE_PROVIDER_translate_json_object_to_puppet_resource = """
    ${name}: json_object['${name}'],
    """

    TEMPLATE_PROVIDER_translate_puppet_resource_to_command_args = """
    args.push('--${name}', puppet_resource[:${name}])
    """

    TEMPLATE_PROVIDER_translate_puppet_resource_to_command_args_namevar = """
    args.push('--${name}', puppet_resource[:${name}]) if mode == 'update'
    """

    TEMPLATE_TYPE_example = """
    ${name} => 'TODO',
    """

    TEMPLATE_TYPE_attributes = """
    ${name}: {
          type: 'String',
          desc: '${help}',
        },
    """

    TEMPLATE_TYPE_attributes_namevar = """
    ${name}: {
          type: 'String',
          desc: '${help}',
          behaviour: :namevar,
        },
    """

    TEMPLATE_TYPE_UNIT_TEST_new_resource = """
    ${name}: 'TODO',
    """

    TEMPLATE_TYPE_UNIT_TEST_accepts_parameter = """
    it 'accepts ${name}' do
          ${click_group}_${click_command}[:${name}] = 'a todo string'
          expect(${click_group}_${click_command}[:${name}]).to eq('a todo string')
        end
    """

    TEMPLATE_PROVIDER_UNIT_TEST_json = """
    "${name}": 'TODO',
    """

    TEMPLATE_PROVIDER_UNIT_TEST_json_namevar = """
    "${name}": 'example ${click_group}_${click_command} TODO_NUMBER',
    """

    TEMPLATE_PROVIDER_UNIT_TEST_ruby_hash = """
    ${name}: 'TODO',
    """

    TEMPLATE_PROVIDER_UNIT_TEST_ruby_hash_namevar = """
    ${name}: 'example ${click_group}_${click_command} TODO_NUMBER',
    """

    TEMPLATE_ACCEPTANCE_TEST_create_item = """
    ${name} => 'TODO',
    """

    TEMPLATE_ACCEPTANCE_TEST_create_item_namevar = ""

    TEMPLATE_ACCEPTANCE_TEST_match_item = """
    expect(r.stdout).to match %r{${name}: TODO}
    """

    TEMPLATE_ACCEPTANCE_TEST_match_item_namevar = """
    expect(r.stdout).to match %r{${name}: acceptance test item}
    """


