import click
import os
from opnsense_cli.commands.new import new
from opnsense_cli.code_generators.opnsense_api.codegenerator import OpnsenseApiCodeGenerator
from opnsense_cli.parser.html_parser import HtmlParser
from opnsense_cli.parser.opnsense_api_reference_parser import OpnsenseApiReferenceParser
from opnsense_cli.parser.opnsense_module_list_parser import OpnsenseModuleListParser
from opnsense_cli.parser.rst_parser import RstParser
from opnsense_cli.template_engines.jinja2 import Jinja2TemplateEngine


@new.group()
def api(**kwargs):
    """
    Generate code for a new api
    """


@api.command()
@click.argument("module_name", required=True)
@click.option(
    "--api-reference-url",
    "-aru",
    help=("The url to the api reference in the official Opnsense documentation"),
    show_default=True,
    default="https://raw.githubusercontent.com/opnsense/docs/master/source/development/api/plugins",
    required=True,
)
@click.option(
    "--api-template-basedir",
    "-atb",
    help="The template basedir path",
    show_default=True,
    default=os.path.join(os.path.dirname(__file__), "../.."),
)
@click.option(
    "--template-api",
    "-ta",
    help="The template for the api relative to the template basedir.",
    show_default=True,
    default="code_generators/opnsense_api/template.py.j2",
)
@click.option(
    "--api-output-dir",
    "-aod",
    help="The output directory for the generated command",
    show_default=True,
    default=os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../output/api/plugins")),
)
def plugin(**kwargs):
    """
    Generate new api code for a plugin module.

    Example:
    Generate api code for the 'haproxy' plugin module

    $ opn-cli new api plugin haproxy

    Default output path is opn-cli/opnsense_cli/output/api/plugins/

    """
    generate_api_files(**kwargs)


@api.command()
@click.argument("module_name", required=True)
@click.option(
    "--api-reference-url",
    "-aru",
    help=("The url to the core module api reference in the official Opnsense documentation."),
    show_default=True,
    default="https://raw.githubusercontent.com/opnsense/docs/master/source/development/api/core",
    required=True,
)
@click.option(
    "--api-template-basedir",
    "-atb",
    help="The template basedir path",
    show_default=True,
    default=os.path.join(os.path.dirname(__file__), "../../../opnsense_cli"),
)
@click.option(
    "--template-api",
    "-ta",
    help="The template for the opnsense api relative to the template basedir.",
    show_default=True,
    default="code_generators/opnsense_api/template.py.j2",
)
@click.option(
    "--api-output-dir",
    "-aod",
    help="The output directory for the generated command",
    show_default=True,
    default=os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../output/api/core")),
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
    generate_api_files(**kwargs)


@api.command()
@click.option(
    "--base-url",
    "-bu",
    help=("The url to the api reference in the official Opnsense documentation."),
    show_default=True,
    default="https://github.com/opnsense/docs/tree/master/source/development/api",
    required=True,
)
@click.option(
    "--module-type",
    "-mt",
    help=("What type of modules to list. core or plugins"),
    type=click.Choice(["core", "plugins"], case_sensitive=True),
    required=True,
)
def list(**kwargs):
    """
    List all plugin or core modules.

    $ opn-cli new api list --module-type core

    $ opn-cli new api list --module-type plugin

    """

    list_modules(f"{kwargs['base_url']}/{kwargs['module_type']}")

def list_modules(url):
    github_html_parser = HtmlParser(url, 'script[type="application/json"][data-target="react-app.embeddedData"]', False)
    parsed_github_html_tag = github_html_parser.parse()
    module_list_parser = OpnsenseModuleListParser(parsed_github_html_tag)
    module_list = module_list_parser.parse()

    for module in module_list:
        click.echo(module)

def generate_api_files(**kwargs):
    rst_url = f"{kwargs['api_reference_url']}/{kwargs['module_name']}.rst"
    rst_parser = RstParser(rst_url, 'table')
    api_reference_tables = rst_parser.parse()

    api_reference_parser = OpnsenseApiReferenceParser(api_reference_tables)
    controller_html_tables = api_reference_parser.parse()
    template_engine = Jinja2TemplateEngine(kwargs["api_template_basedir"])
    write_api(template_engine, controller_html_tables, kwargs['plugin_module_name'], **kwargs)


def write_api(template_engine, controllers, module_name, **kwargs):
    api_code_generator = OpnsenseApiCodeGenerator(
        template_engine=template_engine, template=kwargs["template_api"], controllers=controllers, module_name=module_name
    )
    output_path = f"{kwargs['api_output_dir']}/{module_name}.py"

    click.echo(api_code_generator.write_code(output_path))



