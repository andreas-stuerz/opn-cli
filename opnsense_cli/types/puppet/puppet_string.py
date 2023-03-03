from opnsense_cli.types.puppet.base import PuppetCodeFragment


class PuppetString(PuppetCodeFragment):
    TEMPLATE_translate_json_object_to_puppet_resource = '''
    ${name}: json_object['${name}'],
    '''

    TEMPLATE_translate_puppet_resource_to_command_args = '''
    args.push('--${name}', puppet_resource[:${name}])
    '''
