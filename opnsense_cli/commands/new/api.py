import click
import os
from opnsense_cli.commands.new import new
from opnsense_cli.facades.code_generator.api import ApiCodeGenerator
from opnsense_cli.parser.opnsense_api_reference import OpnsenseApiReferenceParser
from opnsense_cli.parser.opnsense_module_list import OpnsenseModuleListParser
from opnsense_cli.facades.template_engines.jinja2 import Jinja2TemplateEngine


@new.group()
def api(**kwargs):
    """
    Generate code for a new api
    """


@api.command()
@click.argument('plugin_module_name', required=True)
@click.option(
    '--api-reference-url', '-aru',
    help=(
        'The url to the api reference in the official Opnsense documentation'
    ),
    show_default=True,
    default='https://github.com/opnsense/docs/tree/master/source/development/api/plugins',
    required=True
)
@click.option(
    '--api-template-basedir', '-atb',
    help='The template basedir path',
    show_default=True,
    default=os.path.join(os.path.dirname(__file__), '../../templates')
)
@click.option(
    '--template-api', '-ta',
    help='The template for the api relative to the template basedir.',
    show_default=True,
    default='code_generator/api/api.py.j2'
)
@click.option(
    '--api-output-dir', '-aod',
    help='The output directory for the generated command',
    show_default=True,
    default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../output/api/plugins')),
)
def plugin(**kwargs):
    """
    Generate new api code for a plugin module.

    List all plugin module names:

    $ opn-cli new api list --module-type plugin

    Example:
    Generate api code for the 'haproxy' plugin module

    $ opn-cli new api plugin haproxy

    Default output path is opn-cli/opnsense_cli/output/api/plugins/

    """
    generate_api_files(kwargs['plugin_module_name'], **kwargs)


@api.command()
@click.argument('core_module_name', required=True)
@click.option(
    '--api-reference-url', '-aru',
    help=(
        'The url to the core module api reference in the official Opnsense documentation.'
    ),
    show_default=True,
    default='https://github.com/opnsense/docs/tree/master/source/development/api/core',
    required=True
)
@click.option(
    '--api-template-basedir', '-atb',
    help='The template basedir path',
    show_default=True,
    default=os.path.join(os.path.dirname(__file__), '../../../opnsense_cli/templates')
)
@click.option(
    '--template-api', '-ta',
    help='The template for the api relative to the template basedir.',
    show_default=True,
    default='code_generator/api/api.py.j2'
)
@click.option(
    '--api-output-dir', '-aod',
    help='The output directory for the generated command',
    show_default=True,
    default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../output/api/core')),
)
def core(**kwargs):
    """
    Generate new api code for a core module.

    List all core modules:

    $ opn-cli new api list --module-type core

    Example:
    Generate api code for the 'cron' core module

    $ opn-cli new api core cron

    Default output path is opn-cli/opnsense_cli/output/api/core/

    """
    generate_api_files(kwargs['core_module_name'], **kwargs)


@api.command()
@click.option(
    '--base-url', '-bu',
    help=(
        'The url to the api reference in the official Opnsense documentation.'
    ),
    show_default=True,
    default='https://github.com/opnsense/docs/tree/master/source/development/api/',
    required=True
)
@click.option(
    '--module-type', '-mt',
    help=(
        'The url to the api reference in the official Opnsense documentation.'
    ),
    type=click.Choice(['core', 'plugin'], case_sensitive=True),
    required=True
)
def list(**kwargs):
    """

    List all plugin or core modules.

    $ opn-cli new api list --module-type core

    $ opn-cli new api list --module-type plugin

    """
    list_modules(kwargs['module_type'], kwargs['base_url'])


def generate_api_files(module_name, **kwargs):
    controller_parser = OpnsenseApiReferenceParser(
        kwargs['api_reference_url'],
        "table",
        module_name,
        )
    controller_html_tables = controller_parser.parse()
    template_engine = Jinja2TemplateEngine(kwargs['api_template_basedir'])
    write_api(template_engine, controller_html_tables, module_name, **kwargs)


def write_api(template_engine, controllers, module_name, **kwargs):
    api_code_generator = ApiCodeGenerator(
        template_engine=template_engine,
        template=kwargs['template_api'],
        controllers=controllers,
        module_name=module_name
        )
    click.echo(api_code_generator.write_code(kwargs['api_output_dir']))


def list_modules(type, url):
    if type == "core":
        url += "core"
    elif type == "plugin":
        url += "plugins"
    module_list = OpnsenseModuleListParser(url).module_list
    for module in module_list:
        click.echo(module)
