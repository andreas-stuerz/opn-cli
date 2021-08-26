#!/usr/bin/env python3
import click
import os
from opnsense_cli.parser.opnsense_model import OpnsenseModelParser
from opnsense_cli.factories.code_generator.click_option import ClickOptionCodeFactory
from opnsense_cli.facades.code_generator.click_command import ClickCommandCodeGenerator
from opnsense_cli.facades.template_engines.jinja2 import Jinja2TemplateEngine


@click.group()
def command(**kwargs):
    """
    Generate code for a new command by parsing an opnsense model.xml file.
    """

@command.command()
@click.argument('module_name')
@click.option(
    '--base-url', '-b',
    help='The base url.',
    show_default=True,
    default="https://github.com/opnsense/core/tree/master/src/opnsense/mvc/app/models/OPNsense"
)
@click.option(
    '--url-template', '-t',
    help='The template for building the url to the model xml.',
    show_default=True,
    default="{base_url}/{name}/{name}.xml"
)
@click.option(
    '--item', '-i',
    help='The item key from the model.xml to generate the command from.',
    show_default=True,
    required=True
)
@click.option(
    '--template-basedir', '-tb',
    help='The template basedir path',
    show_default=True,
    default=os.path.join(os.path.dirname(__file__), '../opnsense_cli/templates2')
)
@click.option(
    '--template--command', '-tc',
    help='The template for the command relative to the template basedir.',
    show_default=True,
    default='code_generator/command/command.py.j2'
)
def core(**kwargs):
    """
    Generate new command code for a core module.

    For core modules just pass the name of the module e.g. Unbound.

    For a list of core module names see:

    https://docs.opnsense.org/development/api.html#core-api
    """
    print(kwargs)
    name = kwargs['module_name'].lower()
    model_xml_url = kwargs['url_template'].format(
        base_url=kwargs['base_url'], name=kwargs['module_name']
    )
    print(f"Generating code for core module {name} from {model_xml_url} item <{kwargs['item']}></{kwargs['item']}")


@command.command()
@click.argument('click_group')
@click.argument('click_command')
@click.option(
    '--url', '-u',
    help=(
        'The url to the model xml. For net/haproxy e.g. https://raw.githubusercontent.com/opnsense/plugins/blob/master/'
        'net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml'),
    show_default=True,
    required=True
)
@click.option(
    '--tag', '-t',
    help='The xml tag from the model.xml e.g. servers for haproxy backend server command',
    show_default=True,
    required=True
)
@click.option(
    '--template-basedir', '-tb',
    help='The template basedir path',
    show_default=True,
    default=os.path.join(os.path.dirname(__file__), '../opnsense_cli/templates')
)
@click.option(
    '--template-command', '-tc',
    help='The template for the command relative to the template basedir.',
    show_default=True,
    default='code_generator/command/command.py.j2'
)
def plugin(**kwargs):
    """
    Generate new command code for a plugin module.

    Search for model.xml under this url:

    https://github.com/opnsense/plugins
    """
    code_generator = ClickCommandCodeGenerator(
        OpnsenseModelParser(kwargs['url'], kwargs['tag']),
        Jinja2TemplateEngine(kwargs['template_basedir']),
        kwargs['template_command'],
        ClickOptionCodeFactory(),
        kwargs['click_group'],
        kwargs['click_command'],
    )
    code_generator.generate_code()


if __name__ == '__main__':
    command()
