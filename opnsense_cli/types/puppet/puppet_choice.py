from opnsense_cli.types.puppet.base import PuppetCodeFragment


class PuppetChoice(PuppetCodeFragment):
    @property
    def TEMPLATE_TYPE_example(self):
        pass

    @property
    def TEMPLATE_TYPE_attributes(self):
        pass

    TEMPLATE_PROVIDER_translate_json_object_to_puppet_resource = '''
    ${name}: json_object['${name}'],
    '''

    TEMPLATE_PROVIDER_translate_puppet_resource_to_command_args = '''
    args.push('--${name}', puppet_resource[:${name}])
    '''

    TEMPLATE_TYPE_example = '''
    ${name} => 'TODO',
    '''

    TEMPLATE_TYPE_attributes = '''
    ${name}: {
          type: 'Enum["inet", "inet6"]',
          desc: '${help}',
        },
    '''

    TEMPLATE_TYPE_attributes_namevar = '''
    ${name}: {
          type: 'Enum["inet", "inet6"]',
          desc: '${help}',
          behaviour: :namevar,
        },
    '''
