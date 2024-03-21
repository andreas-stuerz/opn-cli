import click
import os
from opnsense_cli.commands.new import new
from opnsense_cli.code_generators.puppet_code.acceptance_test.codegenerator import PuppetAcceptanceTestCodeGenerator
from opnsense_cli.code_generators.puppet_code.provider.codegenerator import PuppetProviderCodeGenerator
from opnsense_cli.code_generators.puppet_code.provider_unit_test.codegenerator import PuppetProviderUnitTestCodeGenerator
from opnsense_cli.code_generators.puppet_code.type.codegenerator import PuppetTypeCodeGenerator
from opnsense_cli.code_generators.puppet_code.type_unit_test.codegenerator import PuppetTypeUnitTestCodeGenerator
from opnsense_cli.template_engines.jinja2 import Jinja2TemplateEngine
from opnsense_cli.cli import cli
from opnsense_cli.code_generators.puppet_code.factories import PuppetCodeFragmentFactory


@new.group()
def puppet(**kwargs):
    """
    Generate puppet code
    """


@puppet.command()
@click.argument("click_group")
@click.argument("click_command")
@click.argument("find_uuid_by_column")
@click.option(
    "--template-basedir",
    "-tb",
    help="The template basedir path",
    show_default=True,
    default=os.path.join(os.path.dirname(__file__), "../../../opnsense_cli"),
)
@click.option(
    "--template-provider",
    "-tp",
    help="The template for the puppet provider relative to the template basedir.",
    show_default=True,
    default="code_generators/puppet_code/provider/template.rb.j2",
)
@click.option(
    "--template-type",
    "-tt",
    help="The template for the puppet type relative to the template basedir.",
    show_default=True,
    default="code_generators/puppet_code/type/template.rb.j2",
)
@click.option(
    "--template-provider-unit-test",
    "-tpt",
    help="The template for the puppet provider unit-test relative to the template basedir.",
    show_default=True,
    default="code_generators/puppet_code/provider_unit_test/template.rb.j2",
)
@click.option(
    "--template-type-unit-test",
    "-ttt",
    help="The template for the puppet type unit-test  relative to the template basedir.",
    show_default=True,
    default="code_generators/puppet_code/type_unit_test/template.rb.j2",
)
@click.option(
    "--template-acceptance-test",
    "-ttt",
    help="The template for the puppet acceptance relative to the template basedir.",
    show_default=True,
    default="code_generators/puppet_code/acceptance_test/template.rb.j2",
)
@click.option(
    "--puppet-output-dir",
    "-pod",
    help="The output directory for the generated puppet resource type files",
    show_default=True,
    default=os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../output/puppet")),
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
    template_engine = Jinja2TemplateEngine(kwargs["template_basedir"])
    code_factory = PuppetCodeFragmentFactory()

    main_group = cli.get_command(ctx, kwargs["click_group"])
    sub_group = main_group.get_command(ctx, kwargs["click_command"])

    create_command = sub_group.get_command(ctx, "create")
    update_command = sub_group.get_command(ctx, "update")

    create_command_params = create_command.to_info_dict(ctx).get("params")
    update_command_params = update_command.to_info_dict(ctx).get("params")

    write_puppet_provider(ctx, template_engine, code_factory, create_command_params, update_command_params, **kwargs)
    write_puppet_type(ctx, template_engine, code_factory, create_command_params, update_command_params, **kwargs)
    write_puppet_type_unit_test(ctx, template_engine, code_factory, create_command_params, update_command_params, **kwargs)
    write_puppet_provider_unit_test(ctx, template_engine, code_factory, create_command_params, update_command_params, **kwargs)
    write_puppet_acceptance_test(ctx, template_engine, code_factory, create_command_params, update_command_params, **kwargs)


def write_puppet_provider(ctx, template_engine, code_factory, create_command_params, update_command_params, **kwargs):
    code_generator = PuppetProviderCodeGenerator(
        template_engine,
        code_factory,
        kwargs["template_provider"],
        kwargs["click_group"],
        kwargs["click_command"],
        kwargs["find_uuid_by_column"],
        create_command_params,
        update_command_params,
    )

    output_path = f"{kwargs['puppet_output_dir']}/provider/opnsense_{kwargs['click_group']}_{kwargs['click_command']}/opnsense_{kwargs['click_group']}_{kwargs['click_command']}.rb"

    click.echo(code_generator.write_code(output_path))


def write_puppet_type(ctx, template_engine, code_factory, create_command_params, update_command_params, **kwargs):
    code_generator = PuppetTypeCodeGenerator(
        template_engine,
        code_factory,
        kwargs["template_type"],
        kwargs["click_group"],
        kwargs["click_command"],
        kwargs["find_uuid_by_column"],
        create_command_params,
        update_command_params,
    )

    output_path = f"{kwargs['puppet_output_dir']}/type/opnsense_{kwargs['click_group']}_{kwargs['click_command']}.rb"

    click.echo(code_generator.write_code(output_path))


def write_puppet_type_unit_test(ctx, template_engine, code_factory, create_command_params, update_command_params, **kwargs):
    code_generator = PuppetTypeUnitTestCodeGenerator(
        template_engine,
        code_factory,
        kwargs["template_type_unit_test"],
        kwargs["click_group"],
        kwargs["click_command"],
        kwargs["find_uuid_by_column"],
        create_command_params,
        update_command_params,
    )

    output_path = f"{kwargs['puppet_output_dir']}/spec/unit/puppet/type/opnsense_{kwargs['click_group']}_{kwargs['click_command']}_spec.rb"

    click.echo(code_generator.write_code(output_path))


def write_puppet_provider_unit_test(
    ctx, template_engine, code_factory, create_command_params, update_command_params, **kwargs
):
    code_generator = PuppetProviderUnitTestCodeGenerator(
        template_engine,
        code_factory,
        kwargs["template_provider_unit_test"],
        kwargs["click_group"],
        kwargs["click_command"],
        kwargs["find_uuid_by_column"],
        create_command_params,
        update_command_params,
    )

    output_path = f"{kwargs['puppet_output_dir']}/spec/unit/puppet/provider/opnsense_{kwargs['click_group']}_{kwargs['click_command']}_spec.rb"

    click.echo(code_generator.write_code(output_path))


def write_puppet_acceptance_test(ctx, template_engine, code_factory, create_command_params, update_command_params, **kwargs):
    code_generator = PuppetAcceptanceTestCodeGenerator(
        template_engine,
        code_factory,
        kwargs["template_acceptance_test"],
        kwargs["click_group"],
        kwargs["click_command"],
        kwargs["find_uuid_by_column"],
        create_command_params,
        update_command_params,
    )

    output_path = f"{kwargs['puppet_output_dir']}/spec/acceptance/types/opnsense_{kwargs['click_group']}_{kwargs['click_command']}_spec.rb"

    click.echo(code_generator.write_code(output_path))


if __name__ == "__main__":
    puppet()
