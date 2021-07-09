import click
from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import formatter_from_formatter_name, bool_as_string, comma_to_newline
from opnsense_cli.commands.firewall import firewall
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.firewall import FirewallFilter
from opnsense_cli.facades.firewall_rule import FirewallRuleFacade

pass_api_client = click.make_pass_decorator(ApiClient)
pass_firewall_rule_svc = click.make_pass_decorator(FirewallRuleFacade)


@firewall.group()
@pass_api_client
@click.pass_context
def rule(ctx, api_client: ApiClient, **kwargs):
    """
    Manage OPNsense firewall rules.

    See: https://docs.opnsense.org/manual/firewall.html

    This Feature need the plugin: os-firewall

    With the new plugin on version 20.1.5 for the firewall API, it adds a new menu item under the "Firewall" section
    called "Automation" under that is the "Filter" menu item.

    All the created firewall rules are above all other rules. The order of execution for the firewall rules goes:
    Automation -> Floating -> Interface


    """
    rule_api = FirewallFilter(api_client)
    ctx.obj = FirewallRuleFacade(rule_api)


@rule.command()
@click.option(
    '--output', '-o',
    help='Specifies the Output format.',
    default="table",
    type=click.Choice(['table', 'json']),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed?',
    default=",".join([
        "uuid,sequence,interface,action,direction,ipprotocol,protocol",
        "source_net,source_port,destination_net,destination_port",
        "description,log,enabled"
    ]),
    show_default=True,
)
@pass_firewall_rule_svc
def list(firewall_rule_svc: FirewallRuleFacade, **kwargs):
    """
    Show all rules
    """
    result = firewall_rule_svc.list_rules()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@rule.command()
@click.argument('rule_sequence')
@click.option(
    '--output', '-o',
    help='Specifies the Output format.',
    default="table",
    type=click.Choice(['table', 'json']),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed?',
    default=",".join([
        "sequence,action,quick,interface,direction,ipprotocol,protocol",
        "source_net,source_not,source_port,destination_net",
        "destination_not,destination_port,gateway,log,description,enabled"
    ]),
    show_default=True,
)
@pass_firewall_rule_svc
def show(firewall_rule_svc: FirewallRuleFacade, **kwargs):
    """
    Show details for alias
    """
    result = firewall_rule_svc.show_rule(kwargs['rule_sequence'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()

# @alias.command()
# @click.argument('name')
# @click.option(
#     '--type', '-t',
#     help='The alias type',
#     type=click.Choice(['host', 'network', 'port', 'url', 'urltable', 'geoip', 'networkgroup', 'mac', 'external']),
#     show_default=True,
#     required=True,
# )
# @click.option(
#     '--content', '-C',
#     help='The alias content. Pass multiple values comma separated. Exclusion starts with “!” sign eg. !192.168.0.0/24',
#     show_default=True,
#     callback=comma_to_newline,
#     required=True,
# )
# @click.option(
#     '--description', '-d',
#     help='The alias description.',
#     show_default=True,
#     required=True,
# )
# @click.option(
#     '--enabled/--disabled',
#     help='Enable or disable alias.',
#     show_default=True,
#     is_flag=True,
#     callback=bool_as_string,
#     default=True,
# )
# @click.option(
#     '--proto', '-p',
#     help='Which ip type should be used? IPv4 and/or IPv6 networks?',
#     type=click.Choice(['', 'IPv4', 'IPv6', 'IPv4,IPv6']),
#     show_default=True,
# )
# @click.option(
#     '--updatefreq', '-u',
#     help='How often should the alias type url_table be updated in days? For every hour specify 1/24: 0.0416666666',
#     type=float,
#     show_default=True,
# )
# @click.option(
#     '--counters/--no-counters',
#     help='Enable or disable pfTable statistics for this alias.',
#     show_default=True,
#     is_flag=True,
#     default=False,
# )
# @click.option(
#     '--output', '-o',
#     help='Specifies the Output format.',
#     default="table",
#     type=click.Choice(['table', 'json']),
#     callback=formatter_from_formatter_name,
#     show_default=True,
# )
# @click.option(
#     '--cols', '-c',
#     help='Which columns should be printed?',
#     default="result,validations",
#     show_default=True,
# )
# @pass_firewall_rule_svc
# def create(firewall_alias_svc: FirewallAliasFacade, **kwargs):
#     """
#     Create a new alias.
#
#     See: https://wiki.opnsense.org/manual/aliases.html
#     """
#     json_payload = {
#         'alias': {
#             "enabled": kwargs['enabled'],
#             "name": kwargs['name'],
#             "type": kwargs['type'],
#             "content": kwargs['content'],
#             "description": kwargs['description'],
#             "proto": kwargs['proto'],
#             "updatefreq": kwargs['updatefreq'],
#             "counters": kwargs['counters'],
#         }
#     }
#
#     result = firewall_alias_svc.create_alias(json_payload)
#
#     CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
#
#
# @alias.command()
# @click.argument('alias_name')
# @click.option(
#     '--name', '-n',
#     help='The new name for the alias.',
#     show_default=True,
# )
# @click.option(
#     '--type', '-t',
#     help='The alias type',
#     type=click.Choice(['host', 'network', 'port', 'url', 'urltable', 'geoip', 'networkgroup', 'mac', 'external']),
#     show_default=True,
# )
# @click.option(
#     '--content', '-C',
#     help='The alias content. Pass multiple values comma separated. Exclusion starts with “!” sign eg. !192.168.0.0/24',
#     show_default=True,
# )
# @click.option(
#     '--description', '-d',
#     help='The alias description.',
#     show_default=True,
# )
# @click.option(
#     '--enabled/--disabled',
#     help='Enable or disable alias.',
#     show_default=True,
#     is_flag=True,
#     callback=bool_as_string,
#     default=None,
# )
# @click.option(
#     '--enabled/--disabled',
#     help='Enable or disable alias.',
#     show_default=True,
#     is_flag=True,
#     default=None
# )
# @click.option(
#     '--proto', '-p',
#     help='Which ip type should be used? IPv4 and/or IPv6 networks?',
#     type=click.Choice(['', 'IPv4', 'IPv6', 'IPv4,IPv6']),
#     show_default=True,
# )
# @click.option(
#     '--updatefreq', '-u',
#     help='How often should the alias type url_table be updated in days? For every hour specify 1/24: 0.0416666666',
#     type=float,
#     show_default=True,
# )
# @click.option(
#     '--counters/--no-counters',
#     help='Enable or disable pfTable statistics for this alias.',
#     show_default=True,
#     is_flag=True,
#     default=None
# )
# @click.option(
#     '--output', '-o',
#     help='Specifies the Output format.',
#     default="table",
#     type=click.Choice(['table', 'json']),
#     callback=formatter_from_formatter_name,
#     show_default=True,
# )
# @click.option(
#     '--cols', '-c',
#     help='Which columns should be printed?',
#     default="result,validations",
#     show_default=True,
# )
# @pass_firewall_rule_svc
# def update(firewall_alias_svc: FirewallAliasFacade, **kwargs):
#     """
#     Update an alias.
#
#     See: https://wiki.opnsense.org/manual/aliases.html
#     """
#     json_payload = {
#         'alias': {'name': kwargs['alias_name']}
#     }
#     options = [
#         'enabled', 'name', 'type', 'content', 'description', 'proto', 'updatefreq', 'counters'
#     ]
#     for option in options:
#         if kwargs[option] is not None:
#             json_payload['alias'][option] = kwargs[option]
#
#     result = firewall_alias_svc.update_alias(kwargs['alias_name'], json_payload)
#
#     CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
#
#
# @alias.command()
# @click.argument('name')
# @click.option(
#     '--output', '-o',
#     help='Specifies the Output format.',
#     default="table",
#     type=click.Choice(['table', 'json']),
#     callback=formatter_from_formatter_name,
#     show_default=True,
# )
# @click.option(
#     '--cols', '-c',
#     help='Which columns should be printed?',
#     default="result,validations",
#     show_default=True,
# )
# @pass_firewall_rule_svc
# def delete(firewall_alias_svc: FirewallAliasFacade, **kwargs):
#     """
#     Delete an alias
#     """
#     result = firewall_alias_svc.delete_alias(kwargs['name'])
#
#     CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
