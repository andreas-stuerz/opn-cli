import click

from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import formatter_from_formatter_name, bool_as_string, int_as_string, available_formats
from opnsense_cli.commands.core.firewall import firewall
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.firewall import FirewallFilter
from opnsense_cli.facades.commands.plugin.firewall.firewall_rule import FirewallRuleFacade

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
    Automation -> Floating -> Interface.

    Before you modify a rule, an automatic config savepoint will be created. if you lock yourself out, the config will
    be rollbacked after 60 seconds.

    See: https://docs.opnsense.org/development/api/plugins/firewall.html#concept

    """
    rule_api = FirewallFilter(api_client)
    ctx.obj = FirewallRuleFacade(rule_api)


@rule.command()
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
    Show all firewall rules
    """
    result = firewall_rule_svc.list_rules()

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@rule.command()
@click.argument('rule_uuid')
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
    Show firewall rule details
    """
    result = firewall_rule_svc.show_rule(kwargs['rule_uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@rule.command()
@click.argument(
    'sequence',
    type=int,
    callback=int_as_string,
)
@click.option(
    '--enabled/--disabled', '--enabled/--no-enabled',
    help='Enable or disable this rule.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
)
@click.option(
    '--action', '-a',
    help='Choose what to do with packets that match the criteria specified.',
    type=click.Choice(['pass', 'block', 'reject']),
    show_default=True,
    default='pass',
    required=True,
)
@click.option(
    '--quick/--no-quick',
    help='If a packet matches a rule specifying quick, then that rule is considered the last matching rule.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=True,
)
@click.option(
    '--interface', '-i',
    help='The network interface(s). Pass multiple values comma separated e.g. lan,wan,lo0',
    show_default=True,
    required=True,
)
@click.option(
    '--direction', '-dir',
    help='Direction of the traffic.',
    type=click.Choice(['in', 'out']),
    show_default=True,
    default='in',
)
@click.option(
    '--ipprotocol', '-ip',
    help='IP Version',
    type=click.Choice(['inet', 'inet6']),
    default='inet',
    show_default=True,
)
@click.option(
    '--protocol', '-p',
    help='Protocol',
    type=click.Choice([
        'any', 'ICMP', 'IGMP', 'GGP', 'IPENCAP', 'ST2', 'TCP', 'CBT', 'EGP', 'IGP', 'BBN-RCC', 'NVP', 'PUP',
        'ARGUS', 'EMCON', 'XNET', 'CHAOS', 'UDP', 'MUX', 'DCN', 'HMP', 'PRM', 'XNS-IDP', 'TRUNK-1', 'TRUNK-2',
        'LEAF-1', 'LEAF-2', 'RDP', 'IRTP', 'ISO-TP4', 'NETBLT', 'MFE-NSP', 'MERIT-INP', 'DCCP', '3PC', 'IDPR',
        'XTP', 'DDP', 'IDPR-CMTP', 'TP++', 'IL', 'IPV6', 'SDRP', 'IDRP', 'RSVP', 'GRE', 'DSR', 'BNA', 'ESP',
        'AH', 'I-NLSP', 'SWIPE', 'NARP', 'MOBILE', 'TLSP', 'SKIP', 'IPV6-ICMP', 'CFTP', 'SAT-EXPAK', 'KRYPTOLAN',
        'RVD', 'IPPC', 'SAT-MON', 'VISA', 'IPCV', 'CPNX', 'CPHB', 'WSN', 'PVP', 'BR-SAT-MON', 'SUN-ND', 'WB-MON',
        'WB-EXPAK', 'ISO-IP', 'VMTP', 'SECURE-VMTP', 'VINES', 'TTP', 'NSFNET-IGP', 'DGP', 'TCF', 'EIGRP', 'OSPF',
        'SPRITE-RPC', 'LARP', 'MTP', 'AX.25', 'IPIP', 'MICP', 'SCC-SP', 'ETHERIP', 'ENCAP', 'GMTP', 'IFMP', 'PNNI',
        'PIM', 'ARIS', 'SCPS', 'QNX', 'A/N', 'IPCOMP', 'SNP', 'COMPAQ-PEER', 'IPX-IN-IP', 'CARP', 'PGM', 'L2TP',
        'DDX', 'IATP', 'STP', 'SRP', 'UTI', 'SMP', 'SM', 'PTP', 'ISIS', 'CRTP', 'CRUDP', 'SPS', 'PIPE', 'SCTP',
        'FC', 'RSVP-E2E-IGNORE', 'UDPLITE', 'MPLS-IN-IP', 'MANET', 'HIP', 'SHIM6', 'WESP', 'ROHC',
        'PFSYNC', 'DIVERT'
        ]),
    default='any',
    show_default=True,
)
@click.option(
    '--source-net', '-src',
    help='The source eg. any, ip address, network or alias.',
    show_default=True,
    required=True,
    default='any'
)
@click.option(
    '--source-port', '-src-port',
    help='Source port number or well known name (imap, imaps, http, https, ...), for ranges use a dash.',
    show_default=True,
    required=True,
    default='',
)
@click.option(
    '--source-not/--no-source-not', '--source-invert/--no-source-invert',
    help='Use this option to invert the sense of the match for the source.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=False,
)
@click.option(
    '--destination-net', '-dst',
    help='The destination eg. any, ip address, network or alias.',
    show_default=True,
    required=True,
    default='any'
)
@click.option(
    '--destination-port', '-dst-port',
    help='Destination port number or well known name (imap, imaps, http, https, ...), for ranges use a dash',
    show_default=True,
    required=True,
    default='',
)
@click.option(
    '--destination-not/--no-destination-not', '--destination-invert/--no-destination-invert',
    help='Use this option to invert the sense of the match for the destination.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=False,
)
@click.option(
    '--gateway', '-g',
    help='Leave as default to use the system routing table. Or choose a gateway to utilize policy based routing.',
    show_default=True,
    required=True,
    default='',
)
@click.option(
    '--log/--no-log',
    help='Log packets that are handled by this rule.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=False,
)
@click.option(
    '--description', '-d',
    help='The rule description.',
    show_default=True,
    required=True,
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
@pass_firewall_rule_svc
def create(firewall_rule_svc: FirewallRuleFacade, **kwargs):
    """
    Create a new firewall rule.

    See: https://docs.opnsense.org/manual/firewall.html
    """
    json_payload = {
        'rule': {
            "enabled": kwargs['enabled'],
            "sequence": kwargs['sequence'],
            "action": kwargs['action'],
            "quick": kwargs['quick'],
            "interface": kwargs['interface'],
            "direction": kwargs['direction'],
            "ipprotocol": kwargs['ipprotocol'],
            "protocol": kwargs['protocol'],
            "source_net": kwargs['source_net'],
            "source_port": kwargs['source_port'],
            "source_not": kwargs['source_not'],
            "destination_net": kwargs['destination_net'],
            "destination_not": kwargs['destination_not'],
            "destination_port": kwargs['destination_port'],
            "gateway": kwargs['gateway'],
            "log": kwargs['log'],
            "description": kwargs['description'],
        }
    }

    result = firewall_rule_svc.create_rule(json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@rule.command()
@click.argument(
    'rule_uuid',
)
@click.option(
    '--sequence', '-s',
    help='The sequence number of this rule.',
    type=int,
    callback=int_as_string,
)
@click.option(
    '--enabled/--disabled',  '--enabled/--no-enabled',
    help='Enable or disable this rule.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None,
)
@click.option(
    '--action', '-a',
    help='Choose what to do with packets that match the criteria specified.',
    type=click.Choice(['pass', 'block', 'reject']),
    show_default=True,
)
@click.option(
    '--quick/--no-quick',
    help='If a packet matches a rule specifying quick, then that rule is considered the last matching rule.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None,
)
@click.option(
    '--interface', '-i',
    help='The network interface(s). Pass multiple values comma separated e.g. lan,wan,lo0',
    show_default=True,
)
@click.option(
    '--direction', '-dir',
    help='Direction of the traffic.',
    type=click.Choice(['in', 'out']),
    show_default=True,
)
@click.option(
    '--ipprotocol', '-ip',
    help='IP Version',
    type=click.Choice(['inet', 'inet6']),
    show_default=True,
)
@click.option(
    '--protocol', '-p',
    help='Protocol',
    type=click.Choice([
        'any', 'ICMP', 'IGMP', 'GGP', 'IPENCAP', 'ST2', 'TCP', 'CBT', 'EGP', 'IGP', 'BBN-RCC', 'NVP', 'PUP',
        'ARGUS', 'EMCON', 'XNET', 'CHAOS', 'UDP', 'MUX', 'DCN', 'HMP', 'PRM', 'XNS-IDP', 'TRUNK-1', 'TRUNK-2',
        'LEAF-1', 'LEAF-2', 'RDP', 'IRTP', 'ISO-TP4', 'NETBLT', 'MFE-NSP', 'MERIT-INP', 'DCCP', '3PC', 'IDPR',
        'XTP', 'DDP', 'IDPR-CMTP', 'TP++', 'IL', 'IPV6', 'SDRP', 'IDRP', 'RSVP', 'GRE', 'DSR', 'BNA', 'ESP',
        'AH', 'I-NLSP', 'SWIPE', 'NARP', 'MOBILE', 'TLSP', 'SKIP', 'IPV6-ICMP', 'CFTP', 'SAT-EXPAK', 'KRYPTOLAN',
        'RVD', 'IPPC', 'SAT-MON', 'VISA', 'IPCV', 'CPNX', 'CPHB', 'WSN', 'PVP', 'BR-SAT-MON', 'SUN-ND', 'WB-MON',
        'WB-EXPAK', 'ISO-IP', 'VMTP', 'SECURE-VMTP', 'VINES', 'TTP', 'NSFNET-IGP', 'DGP', 'TCF', 'EIGRP', 'OSPF',
        'SPRITE-RPC', 'LARP', 'MTP', 'AX.25', 'IPIP', 'MICP', 'SCC-SP', 'ETHERIP', 'ENCAP', 'GMTP', 'IFMP', 'PNNI',
        'PIM', 'ARIS', 'SCPS', 'QNX', 'A/N', 'IPCOMP', 'SNP', 'COMPAQ-PEER', 'IPX-IN-IP', 'CARP', 'PGM', 'L2TP',
        'DDX', 'IATP', 'STP', 'SRP', 'UTI', 'SMP', 'SM', 'PTP', 'ISIS', 'CRTP', 'CRUDP', 'SPS', 'PIPE', 'SCTP',
        'FC', 'RSVP-E2E-IGNORE', 'UDPLITE', 'MPLS-IN-IP', 'MANET', 'HIP', 'SHIM6', 'WESP', 'ROHC',
        'PFSYNC', 'DIVERT'
    ]),
    show_default=True,
)
@click.option(
    '--source-net', '-src',
    help='The source eg. any, ip address, network or alias.',
    show_default=True,
)
@click.option(
    '--source-port', '-src-port',
    help='Source port number or well known name (imap, imaps, http, https, ...), for ranges use a dash.',
    show_default=True,
)
@click.option(
    '--source-not/--no-source-not', '--source-invert/--no-source-invert',
    help='Use this option to invert the sense of the match for the source.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None,
)
@click.option(
    '--destination-net', '-dst',
    help='The destination eg. any, ip address, network or alias.',
    show_default=True,
)
@click.option(
    '--destination-port', '-dst-port',
    help='Destination port number or well known name (imap, imaps, http, https, ...), for ranges use a dash',
    show_default=True,
)
@click.option(
    '--destination-not/--no-destination-not', '--destination-invert/--no-destination-invert',
    help='Use this option to invert the sense of the match for the destination.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None,
)
@click.option(
    '--gateway', '-g',
    help='Leave as default to use the system routing table. Or choose a gateway to utilize policy based routing.',
    show_default=True,
)
@click.option(
    '--log/--no-log',
    help='Log packets that are handled by this rule.',
    show_default=True,
    is_flag=True,
    callback=bool_as_string,
    default=None,
)
@click.option(
    '--description', '-d',
    help='The rule description.',
    show_default=True,
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
@pass_firewall_rule_svc
def update(firewall_rule_svc: FirewallRuleFacade, **kwargs):
    """
    Update firewall rule.

    See: https://docs.opnsense.org/manual/firewall.html
    """
    json_payload = {
        'rule': {}
    }
    options = [
        'sequence', 'action', 'source_net', 'direction', 'destination_net', 'destination_not', 'destination_port',
        'source_not', 'protocol', 'interface', 'gateway', 'log', 'enabled', 'description', 'source_port',
        'ipprotocol', 'quick'
    ]
    for option in options:
        if kwargs[option] is not None:
            json_payload['rule'][option] = kwargs[option]

    result = firewall_rule_svc.update_rule(kwargs['rule_uuid'], json_payload)

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@rule.command()
@click.argument('rule_uuid')
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
@pass_firewall_rule_svc
def delete(firewall_rule_svc: FirewallRuleFacade, **kwargs):
    """
    Delete a firewall rule
    """
    result = firewall_rule_svc.delete_rule(kwargs['rule_uuid'])

    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
