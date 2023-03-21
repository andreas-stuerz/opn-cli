import click
import os
from opnsense_cli.commands.new import new
from opnsense_cli.facades.code_generator.puppet_acceptance_test import PuppetAcceptanceTestCodeGenerator
from opnsense_cli.facades.code_generator.puppet_provider import PuppetProviderCodeGenerator
from opnsense_cli.facades.code_generator.puppet_provider_unit_test import PuppetProviderUnitTestCodeGenerator
from opnsense_cli.facades.code_generator.puppet_type import PuppetTypeCodeGenerator
from opnsense_cli.facades.code_generator.puppet_type_unit_test import PuppetTypeUnitTestCodeGenerator
from opnsense_cli.facades.template_engines.jinja2 import Jinja2TemplateEngine
from opnsense_cli.cli import cli
from opnsense_cli.factories.code_generator.puppet_code_fragment import PuppetCodeFragmentFactory


@new.group()
def puppet(**kwargs):
    """
    Generate puppet code
    """


@puppet.command()
@click.argument('click_group')
@click.argument('click_command')
@click.argument('find_uuid_by_column')
@click.option(
    '--template-basedir', '-tb',
    help='The template basedir path',
    show_default=True,
    default=os.path.join(os.path.dirname(__file__), '../../../opnsense_cli/templates')
)
@click.option(
    '--template-provider', '-tp',
    help='The template for the puppet provider relative to the template basedir.',
    show_default=True,
    default='code_generator/puppet/provider.rb.j2'
)
@click.option(
    '--template-type', '-tt',
    help='The template for the puppet type relative to the template basedir.',
    show_default=True,
    default='code_generator/puppet/type.rb.j2'
)
@click.option(
    '--template-provider-unit-test', '-tpt',
    help='The template for the puppet provider unit-test relative to the template basedir.',
    show_default=True,
    default='code_generator/puppet/provider_unit_test.rb.j2'
)
@click.option(
    '--template-type-unit-test', '-ttt',
    help='The template for the puppet type unit-test  relative to the template basedir.',
    show_default=True,
    default='code_generator/puppet/type_unit_test.rb.j2'
)
@click.option(
    '--template-acceptance-test', '-ttt',
    help='The template for the puppet acceptance relative to the template basedir.',
    show_default=True,
    default='code_generator/puppet/acceptance_test.rb.j2'
)
@click.option(
    '--puppet-output-dir', '-pod',
    help='The output directory for the generated puppet resource type files',
    show_default=True,
    default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../output/puppet')),
)
@click.option(
    '--provider-output-dir', '-pod',
    help='The output directory for the generated puppet provider',
    show_default=True,
    default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../output/puppet/provider')),
)
@click.option(
    '--type-output-dir', '-pod',
    help='The output directory for the generated puppet provider',
    show_default=True,
    default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../output/puppet/type')),
)
@click.option(
    '--provider-test-output-dir', '-ptod',
    help='The output directory for the generated provider unit test',
    show_default=True,
    default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../output/puppet/spec/unit/puppet/provider')),
)
@click.option(
    '--type-test-output-dir', '-ttod',
    help='The output directory for the generated type unit test',
    show_default=True,
    default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../output/puppet/spec/unit/puppet/type')),
)
@click.option(
    '--acceptance-test-output-dir', '-atod',
    help='The output directory for the generated resource type acceptance test',
    show_default=True,
    default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../output/puppet/spec/acceptance/types')),
)
@click.pass_context
def resource_type(ctx, **kwargs):
    """
    Generate a new puppet resource type from an existing opn-cli command

    Create provider, type, unit and acceptance tests for a new puppet resource type.

    Example:

    > opn-cli new puppet resource-type route static descr

    creates a puppet reource type for the opn-cli command:
    > opn-cli route static

    And use the column "descr" as the puppet resource namevar.
    The puppet resource will be unqiue by the descr column and will be used to find the uuid.

    """
    generate_puppet_files(ctx, **kwargs)


def generate_puppet_files(ctx, **kwargs):
    template_engine = Jinja2TemplateEngine(kwargs['template_basedir'])
    code_factory = PuppetCodeFragmentFactory()

    main_group = cli.get_command(ctx, kwargs['click_group'])
    sub_group = main_group.get_command(ctx, kwargs['click_command'])

    create_command = sub_group.get_command(ctx, 'create')
    update_command = sub_group.get_command(ctx, 'update')

    create_command_params = create_command.to_info_dict(ctx).get('params')
    update_command_params = update_command.to_info_dict(ctx).get('params')

    write_puppet_provider(ctx, template_engine, code_factory, create_command_params, update_command_params, **kwargs)
    write_puppet_type(ctx, template_engine, code_factory, create_command_params, update_command_params, **kwargs)
    write_puppet_type_unit_test(ctx, template_engine, code_factory, create_command_params, update_command_params, **kwargs)
    write_puppet_provider_unit_test(ctx, template_engine, code_factory, create_command_params, update_command_params, **kwargs)
    write_puppet_acceptance_test(ctx, template_engine, code_factory, create_command_params, update_command_params, **kwargs)


def write_puppet_provider(
        ctx,
        template_engine,
        code_factory,
        create_command_params,
        update_command_params,
        **kwargs
):
    code_generator = PuppetProviderCodeGenerator(
        template_engine,
        code_factory,
        kwargs['template_provider'],
        kwargs['click_group'],
        kwargs['click_command'],
        kwargs['find_uuid_by_column'],
        create_command_params,
        update_command_params,
    )

    click.echo(
        code_generator.write_code(kwargs['provider_output_dir'])
    )


def write_puppet_type(
    ctx,
    template_engine,
    code_factory,
    create_command_params,
    update_command_params,
    **kwargs
):
    code_generator = PuppetTypeCodeGenerator(
        template_engine,
        code_factory,
        kwargs['template_type'],
        kwargs['click_group'],
        kwargs['click_command'],
        kwargs['find_uuid_by_column'],
        create_command_params,
        update_command_params,
    )

    click.echo(
        code_generator.write_code(kwargs['type_output_dir'])
    )


def write_puppet_type_unit_test(
        ctx,
        template_engine,
        code_factory,
        create_command_params,
        update_command_params,
        **kwargs
):
    code_generator = PuppetTypeUnitTestCodeGenerator(
        template_engine,
        code_factory,
        kwargs['template_type_unit_test'],
        kwargs['click_group'],
        kwargs['click_command'],
        kwargs['find_uuid_by_column'],
        create_command_params,
        update_command_params,
    )

    click.echo(
        code_generator.write_code(kwargs['type_test_output_dir'])
    )


def write_puppet_provider_unit_test(
        ctx,
        template_engine,
        code_factory,
        create_command_params,
        update_command_params,
        **kwargs
):
    code_generator = PuppetProviderUnitTestCodeGenerator(
        template_engine,
        code_factory,
        kwargs['template_provider_unit_test'],
        kwargs['click_group'],
        kwargs['click_command'],
        kwargs['find_uuid_by_column'],
        create_command_params,
        update_command_params,
    )

    click.echo(
        code_generator.write_code(kwargs['provider_test_output_dir'])
    )


def write_puppet_acceptance_test(
        ctx,
        template_engine,
        code_factory,
        create_command_params,
        update_command_params,
        **kwargs
):
    code_generator = PuppetAcceptanceTestCodeGenerator(
        template_engine,
        code_factory,
        kwargs['template_acceptance_test'],
        kwargs['click_group'],
        kwargs['click_command'],
        kwargs['find_uuid_by_column'],
        create_command_params,
        update_command_params,
    )

    click.echo(
        code_generator.write_code(kwargs['acceptance_test_output_dir'])
    )


if __name__ == '__main__':
    puppet()
