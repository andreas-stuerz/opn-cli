from opnsense_cli.types.puppet.base import PuppetCodeFragment


class PuppetBoolean(PuppetCodeFragment):
    TEMPLATE_PROVIDER_translate_json_object_to_puppet_resource = '''
    ${name}: bool_from_value(json_object['${name}']),
    '''

    TEMPLATE_PROVIDER_translate_puppet_resource_to_command_args = '''
    args.push('--${name}') if bool_from_value(puppet_resource[:${name}]) == true
            args.push('--no-${name}') if bool_from_value(puppet_resource[:${name}]) == false
    '''

    TEMPLATE_TYPE_example = '''
    ${name} => TODO,
    '''

    TEMPLATE_TYPE_attributes = '''
    ${name}: {
          type: 'Boolean',
          desc: '${help}',
        },
    '''

    TEMPLATE_TYPE_attributes_namevar = '''
    ${name}: {
          type: 'Boolean',
          desc: '${help}',
          behaviour: :namevar,
        },
    '''

    TEMPLATE_TYPE_UNIT_TEST_new_resource = '''
    ${name}: true,
    '''

    TEMPLATE_TYPE_UNIT_TEST_accepts_parameter = '''
    it 'accepts ${name}' do
          ${click_group}_{click_command}[:${name}] = false
          expect(${click_group}_{click_command}[:${name}]).to eq(:false)
        end
    '''


    TEMPLATE_PROVIDER_UNIT_TEST_json = '''
    "${name}": '1',
    '''

    TEMPLATE_PROVIDER_UNIT_TEST_ruby_hash = '''
    ${name}: true,
    '''
