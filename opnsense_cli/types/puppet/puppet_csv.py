from opnsense_cli.types.puppet.base import PuppetCodeFragment


class PuppetCsv(PuppetCodeFragment):
    TEMPLATE_PROVIDER_translate_json_object_to_puppet_resource = '''
    ${name}: array_from_value(json_object['${name}']),
    '''

    TEMPLATE_PROVIDER_translate_puppet_resource_to_command_args = '''
    args.push('--${name}', puppet_resource[:${name}].join(','))
    '''

    TEMPLATE_TYPE_example = '''
    ${name} => [],
    '''

    TEMPLATE_TYPE_attributes = '''
    ${name}: {
          type: "Array[String]",
          desc: '${help}',
          default: []
        },
    '''

    TEMPLATE_TYPE_UNIT_TEST_new_resource = '''
    ${name}: [],
    '''

    TEMPLATE_TYPE_UNIT_TEST_accepts_parameter = '''
    it 'accepts ${name}' do
          ${click_group}_{click_command}[:${name}] = ['valid item1', 'valid item2']
          expect(${click_group}_{click_command}[:${name}]).to eq(['valid item1', 'valid item2'])
        end
    '''

    TEMPLATE_PROVIDER_UNIT_TEST_json = '''
    "${name}": 'TODO_CSV',
    '''

    TEMPLATE_PROVIDER_UNIT_TEST_ruby_hash = '''
    ${name}: ['TODO_CSV'],
    '''

    TEMPLATE_ACCEPTANCE_TEST_create_item = '''
    ${name} => [],
    '''

    TEMPLATE_ACCEPTANCE_TEST_match_item = '''
    expect(r.stdout).to match %r{${name}: '\\[\\]'}
    '''
