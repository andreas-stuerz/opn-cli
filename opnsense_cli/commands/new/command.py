import click
import os
from opnsense_cli.facades.code_generator.click_command_facade import ClickCommandFacadeCodeGenerator
from opnsense_cli.facades.code_generator.click_command_test_unit import ClickCommandTestCodeGenerator
from opnsense_cli.parser.opnsense_form import OpnsenseFormParser
from opnsense_cli.parser.opnsense_model import OpnsenseModelParser
from opnsense_cli.factories.code_generator.click_option import ClickOptionCodeTypeFactory
from opnsense_cli.facades.code_generator.click_command import ClickCommandCodeGenerator
from opnsense_cli.facades.template_engines.jinja2 import Jinja2TemplateEngine
from bs4.element import Tag


@click.group()
def command(**kwargs):
    """
    Generate code for a new command
    """


@command.command()
@click.argument('click_group')
@click.argument('click_command')
@click.option(
    '--model-url', '-m',
    help=(
        'The url to the model xml. For core unbound e.g. https://raw.githubusercontent.com'
        '/opnsense/core/master/src/opnsense/mvc/app/models/OPNsense/Unbound/Unbound.xml'
    ),
    show_default=True,
    required=True
)
@click.option(
    '--tag', '-t',
    help='The xml tag from the model.xml e.g. dnsbl for unbound dnsbl command',
    show_default=True,
    required=True
)
@click.option(
    '--form-url', '-f',
    help=(
        'The url to the form xml for parsing the help texts. '
        'For net/haproxy server e.g. https://raw.githubusercontent.com/opnsense/plugins/'
        'master/net/haproxy/src/opnsense/mvc/app/controllers/OPNsense/HAProxy/forms/dialogServer.xml'
    ),
    show_default=True,
    required=True
)
@click.option(
    '--template-basedir', '-tb',
    help='The template basedir path',
    show_default=True,
    default=os.path.join(os.path.dirname(__file__), '../../../opnsense_cli/templates')
)
@click.option(
    '--template-command', '-tc',
    help='The template for the command relative to the template basedir.',
    show_default=True,
    default='code_generator/command/command.py.j2'
)
@click.option(
    '--template-facade', '-tf',
    help='The template for the command facade relative to the template basedir.',
    show_default=True,
    default='code_generator/command/command_facade.py.j2'
)
@click.option(
    '--template-test', '-tt',
    help='The template for the command test relative to the template basedir.',
    show_default=True,
    default='code_generator/command/command_test.py.j2'
)
@click.option(
    '--command-output-dir', '-cod',
    help='The output directory for the generated command',
    show_default=True,
    default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../output/commands/core')),
)
@click.option(
    '--facade-output-dir', '-fod',
    help='The output directory for the generated facade',
    show_default=True,
    default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../output/facades/command/core')),
)
@click.option(
    '--test-output-dir', '-tod',
    help='The output directory for the generated test',
    show_default=True,
    default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../output/test/commands/core')),
)
def core(**kwargs):
    """
    Generate new command code for a core module.

    For a list of core modules see:

    https://docs.opnsense.org/development/api.html#core-api

    Search model.xml files here:

    https://github.com/opnsense/core/tree/master/src/opnsense/mvc/app/models/OPNsense

    Example:

    $ opn-cli new command core unbound dnsbl --tag dnsbl \

    --url https://raw.githubusercontent.com/opnsense/core/master/src/opnsense/mvc/app/models/OPNsense/Unbound/Unbound.xml
    """
    generate_command_files('core', **kwargs)


@command.command()
@click.argument('click_group')
@click.argument('click_command')
@click.option(
    '--model-url', '-m',
    help=(
        'The url to the model xml. For net/haproxy e.g. https://raw.githubusercontent.com/opnsense/plugins/blob/master/'
        'net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml'),
    show_default=True,
    required=True
)
@click.option(
    '--tag', '-t',
    help='The xml tag from the model.xml e.g. servers for haproxy server command',
    show_default=True,
    required=True
)
@click.option(
    '--form-url', '-f',
    help=(
        'The url to the form xml for parsing the help texts. '
        'For net/haproxy server e.g. https://raw.githubusercontent.com/opnsense/plugins/'
        'master/net/haproxy/src/opnsense/mvc/app/controllers/OPNsense/HAProxy/forms/dialogServer.xml'
    ),
    show_default=True,
)
@click.option(
    '--template-basedir', '-tb',
    help='The template basedir path',
    show_default=True,
    default=os.path.join(os.path.dirname(__file__), '../../../opnsense_cli/templates')
)
@click.option(
    '--template-command', '-tc',
    help='The template for the command relative to the template basedir.',
    show_default=True,
    default='code_generator/command/command.py.j2'
)
@click.option(
    '--template-facade', '-tf',
    help='The template for the command facade relative to the template basedir.',
    show_default=True,
    default='code_generator/command/command_facade.py.j2'
)
@click.option(
    '--template-test', '-tt',
    help='The template for the command test relative to the template basedir.',
    show_default=True,
    default='code_generator/command/command_test.py.j2'
)
@click.option(
    '--command-output-dir', '-cod',
    help='The output directory for the generated command',
    show_default=True,
    default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../output/commands/plugin')),
)
@click.option(
    '--facade-output-dir', '-fod',
    help='The output directory for the generated facade',
    show_default=True,
    default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../output/facades/command/plugin')),
)
@click.option(
    '--test-output-dir', '-tod',
    help='The output directory for the generated test',
    show_default=True,
    default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../output/test/commands/plugin')),
)
def plugin(**kwargs):
    """
    Generate new command code for a plugin module.

    For a list of plugin modules see:

    https://docs.opnsense.org/development/api.html#plugins-api

    Search for model.xml and form.xml files here:

    https://github.com/opnsense/plugins

    Example:

    $ opn-cli new command plugin haproxy server --tag servers \
    -m https://raw.githubusercontent.com/opnsense/plugins/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/
    HAProxy/HAProxy.xml \
    -f https://raw.githubusercontent.com/opnsense/plugins/master/net/haproxy/src/opnsense/mvc/app/controllers/OPNsense/
    HAProxy/forms/dialogServer.xml

    """
    generate_command_files('plugin', **kwargs)


def generate_command_files(type, **kwargs):
    model_tag = OpnsenseModelParser(kwargs['model_url'], kwargs['tag']).parse()
    template_engine = Jinja2TemplateEngine(kwargs['template_basedir'])
    option_factory = ClickOptionCodeTypeFactory()

    write_command(type, model_tag, template_engine, option_factory, **kwargs)
    write_command_facade(type, model_tag, template_engine, option_factory, **kwargs)
    write_command_test(type, model_tag, template_engine, option_factory, **kwargs)


def write_command(type, model_tag: Tag, template_engine, option_factory, **kwargs):
    command_code_generator = ClickCommandCodeGenerator(
        model_tag,
        template_engine,
        option_factory,
        kwargs['template_command'],
        kwargs['click_group'],
        kwargs['click_command'],
        kwargs['tag'],
        type,
    )

    if kwargs['form_url']:
        form_parser = OpnsenseFormParser(kwargs['form_url'], 'form')
        command_code_generator.help_messages = form_parser.parse()

    click.echo(
        command_code_generator.write_code(kwargs['command_output_dir'])
    )


def write_command_facade(type, model_tag: Tag, template_engine, option_factory, **kwargs):
    command_facade_generator = ClickCommandFacadeCodeGenerator(
        model_tag,
        template_engine,
        option_factory,
        kwargs['template_facade'],
        kwargs['click_group'],
        kwargs['click_command'],
        kwargs['tag'],
        type,
    )
    click.echo(
        command_facade_generator.write_code(kwargs['facade_output_dir'])
    )


def write_command_test(type, model_tag: Tag, template_engine, option_factory, **kwargs):
    command_test_generator = ClickCommandTestCodeGenerator(
        model_tag,
        template_engine,
        option_factory,
        kwargs['template_test'],
        kwargs['click_group'],
        kwargs['click_command'],
        kwargs['tag'],
        type,
    )
    click.echo(
        command_test_generator.write_code(
            kwargs['test_output_dir'], filename_prefix=f"test_{kwargs['click_group']}_"
        )
    )


if __name__ == '__main__':
    command()
