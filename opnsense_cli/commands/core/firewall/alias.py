import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import \
    formatter_from_formatter_name, bool_as_string, comma_to_newline, available_formats
from opnsense_cli.commands.core.firewall import firewall
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.firewall import FirewallAlias, FirewallAliasUtil
from opnsense_cli.facades.commands.core.firewall.firewall_alias import FirewallAliasFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_firewall_alias_svc = click.make_pass_decorator(FirewallAliasFacade)


@firewall.group()
@pass_api_client
@click.pass_context
def alias(ctx, api_client: ApiClient, **kwargs):
    """
    Manage OPNsense firewall aliases.

    See: https://wiki.opnsense.org/manual/aliases.html
    """
    alias_api = FirewallAlias(api_client)
    alias_util_api = FirewallAliasUtil(api_client)
    ctx.obj = FirewallAliasFacade(alias_api, alias_util_api)


@alias.command()
@click.option(
    '--output', '-o',
    help='Specifies the Output format.',
    default="table",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    default="name,type,description,content,enabled",
    show_default=True,
)
@pass_firewall_alias_svc
def list(firewall_alias_svc: FirewallAliasFacade, **kwargs):
    """
    Show all aliases
    """
    result = firewall_alias_svc.list_aliases()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@alias.command()
@click.argument('alias_name')
@click.option(
    '--output', '-o',
    help='Specifies the Output format.',
    default="table",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    default="uuid,name,type,proto,counters,description,updatefreq,content,enabled",
    show_default=True,
)
@pass_firewall_alias_svc
def show(firewall_alias_svc: FirewallAliasFacade, **kwargs):
    """
    Show details for alias
    """
    result = firewall_alias_svc.show_alias(kwargs['alias_name'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@alias.command()
@click.argument('alias_name')
@click.option(
    '--output', '-o',
    help='Specifies the Output format.',
    default="table",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    default="ip",
    show_default=True,
)
@pass_firewall_alias_svc
def table(firewall_alias_svc: FirewallAliasFacade, **kwargs):
    """
    Show pf table entries for alias
    """
    result = firewall_alias_svc.show_pf_table(kwargs['alias_name'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@alias.command()
@click.argument('name')
@click.option(
    '--type', '-t',
    help='The alias type',
    type=click.Choice(['host', 'network', 'port', 'url', 'urltable', 'geoip', 'networkgroup', 'mac', 'external']),
    show_default=True,
    required=True,
)
@click.option(
    '--content', '-C',
    help='The alias content. Pass multiple values comma separated. Exclusion starts with “!” sign eg. !192.168.0.0/24',
    show_default=True,
    callback=comma_to_newline,
    required=True,
)
@click.option(
    '--description', '-d',
    help='The alias description.',
    show_default=True,
    required=True,
)
@click.option(
    '--enabled/--disabled', '--enabled/--no-enabled',
    help='Enable or disable alias.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
)
@click.option(
    '--proto', '-p',
    help='Which ip type should be used? IPv4 and/or IPv6 networks?',
    type=click.Choice(['', 'IPv4', 'IPv6', 'IPv4,IPv6']),
    show_default=True,
)
@click.option(
    '--updatefreq', '-u',
    help='How often should the alias type url_table be updated in days? For every hour specify 1/24: 0.0416666666',
    type=float,
    show_default=True,
)
@click.option(
    '--counters/--no-counters',
    help='Enable or disable pfTable statistics for this alias.',
    show_default=True,
    is_flag=True,
    default=False,
)
@click.option(
    '--output', '-o',
    help='Specifies the Output format.',
    default="plain",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    default="result,validations",
    show_default=True,
)
@pass_firewall_alias_svc
def create(firewall_alias_svc: FirewallAliasFacade, **kwargs):
    """
    Create a new alias.

    See: https://wiki.opnsense.org/manual/aliases.html
    """
    json_payload = {
        'alias': {
            "enabled": kwargs['enabled'],
            "name": kwargs['name'],
            "type": kwargs['type'],
            "content": kwargs['content'],
            "description": kwargs['description'],
            "proto": kwargs['proto'],
            "updatefreq": kwargs['updatefreq'],
            "counters": kwargs['counters'],
        }
    }

    result = firewall_alias_svc.create_alias(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@alias.command()
@click.argument('alias_name')
@click.option(
    '--name', '-n',
    help='The new name for the alias.',
    show_default=True,
)
@click.option(
    '--type', '-t',
    help='The alias type',
    type=click.Choice(['host', 'network', 'port', 'url', 'urltable', 'geoip', 'networkgroup', 'mac', 'external']),
    show_default=True,
)
@click.option(
    '--content', '-C',
    help='The alias content. Pass multiple values comma separated. Exclusion starts with “!” sign eg. !192.168.0.0/24',
    show_default=True,
    callback=comma_to_newline,
)
@click.option(
    '--description', '-d',
    help='The alias description.',
    show_default=True,
)
@click.option(
    '--enabled/--disabled', '--enabled/--no-enabled',
    help='Enable or disable alias.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None,
)
@click.option(
    '--enabled/--disabled', '--enabled/--no-enabled',
    help='Enable or disable alias.',
    show_default=True,
    is_flag=True,
    default=None
)
@click.option(
    '--proto', '-p',
    help='Which ip type should be used? IPv4 and/or IPv6 networks?',
    type=click.Choice(['', 'IPv4', 'IPv6', 'IPv4,IPv6']),
    show_default=True,
)
@click.option(
    '--updatefreq', '-u',
    help='How often should the alias type url_table be updated in days? For every hour specify 1/24: 0.0416666666',
    type=float,
    show_default=True,
)
@click.option(
    '--counters/--no-counters',
    help='Enable or disable pfTable statistics for this alias.',
    show_default=True,
    is_flag=True,
    default=None
)
@click.option(
    '--output', '-o',
    help='Specifies the Output format.',
    default="plain",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    default="result,validations",
    show_default=True,
)
@pass_firewall_alias_svc
def update(firewall_alias_svc: FirewallAliasFacade, **kwargs):
    """
    Update an alias.

    See: https://wiki.opnsense.org/manual/aliases.html
    """
    json_payload = {
        'alias': {'name': kwargs['alias_name']}
    }
    options = [
        'enabled', 'name', 'type', 'content', 'description', 'proto', 'updatefreq', 'counters'
    ]
    for option in options:
        if kwargs[option] is not None:
            json_payload['alias'][option] = kwargs[option]

    result = firewall_alias_svc.update_alias(kwargs['alias_name'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@alias.command()
@click.argument('name')
@click.option(
    '--output', '-o',
    help='Specifies the Output format.',
    default="plain",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    default="result,validations",
    show_default=True,
)
@pass_firewall_alias_svc
def delete(firewall_alias_svc: FirewallAliasFacade, **kwargs):
    """
    Delete an alias
    """
    result = firewall_alias_svc.delete_alias(kwargs['name'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
