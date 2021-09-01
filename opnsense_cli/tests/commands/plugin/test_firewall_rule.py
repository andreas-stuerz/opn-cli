from unittest.mock import patch, Mock
from opnsense_cli.commands.plugin.firewall.rule import rule
from opnsense_cli.tests.commands.base import CommandTestCase


class TestFirewallRuleCommands(CommandTestCase):
    def setUp(self):
        self._api_data_fixtures_savepoint_OK = {
            "status": "ok",
            "retention": "60",
            "revision": "1626265654.2136"
        }
        self._api_data_fixtures_savepoint_FAILED = {
            "status": "failed",
        }
        self._api_data_fixtures_apply_OK = {
            "status": "OK\n\n",
        }
        self._api_data_fixtures_apply_FAILED = {
            "status": "FAILED\n\n",
        }
        self._api_data_fixtures_cancel_rollback_OK = {
            "status": "\n\n",
        }
        self._api_data_fixtures_cancel_rollback_FAILED = {
            "status": "failed\n\n",
        }

        self._api_data_fixtures_create_OK = {
            "result": "saved",
            "uuid": "85282721-934c-42be-ba4d-a93cbfda26af"
        }
        self._api_data_fixtures_create_ERROR = {
            "result": "failed",
            "validations": {"rule.source_net": "alias_not_exists is not a valid source IP address or alias."}
        }
        self._api_data_fixtures_update_OK = {
            "result": "saved"
        }
        self._api_data_fixtures_update_NOT_EXISTS = {
            "result": "failed"
        }
        self._api_data_fixtures_delete_NOT_FOUND = {
            "result": "not found"
        }
        self._api_data_fixtures_delete_OK = {
            "result": "deleted"
        }
        self._api_data_fixtures_list = {
            "filter": {
                "rules": {
                    "rule": {
                        "b468c719-89db-45a8-bd02-b081246dc002": {
                            "enabled": "1",
                            "sequence": "1",
                            "action": {
                                "pass": {
                                    "value": "Pass",
                                    "selected": 1
                                },
                                "block": {
                                    "value": "Block",
                                    "selected": 0
                                },
                                "reject": {
                                    "value": "Reject",
                                    "selected": 0
                                }
                            },
                            "quick": "1",
                            "interface": {
                                "lan": {
                                    "value": "LAN",
                                    "selected": 1
                                },
                                "lo0": {
                                    "value": "Loopback",
                                    "selected": 0
                                },
                                "wan": {
                                    "value": "WAN",
                                    "selected": 0
                                }
                            },
                            "direction": {
                                "in": {
                                    "value": "In",
                                    "selected": 1
                                },
                                "out": {
                                    "value": "Out",
                                    "selected": 0
                                }
                            },
                            "ipprotocol": {
                                "inet": {
                                    "value": "IPv4",
                                    "selected": 1
                                },
                                "inet6": {
                                    "value": "IPv6",
                                    "selected": 0
                                }
                            },
                            "protocol": {
                                "any": {
                                    "value": "any",
                                    "selected": 0
                                },
                                "ICMP": {
                                    "value": "ICMP",
                                    "selected": 0
                                },
                                "IGMP": {
                                    "value": "IGMP",
                                    "selected": 0
                                },
                                "GGP": {
                                    "value": "GGP",
                                    "selected": 0
                                },
                                "IPENCAP": {
                                    "value": "IPENCAP",
                                    "selected": 0
                                },
                                "ST2": {
                                    "value": "ST2",
                                    "selected": 0
                                },
                                "TCP": {
                                    "value": "TCP",
                                    "selected": 1
                                },
                                "CBT": {
                                    "value": "CBT",
                                    "selected": 0
                                },
                                "EGP": {
                                    "value": "EGP",
                                    "selected": 0
                                },
                                "IGP": {
                                    "value": "IGP",
                                    "selected": 0
                                },
                                "BBN-RCC": {
                                    "value": "BBN-RCC",
                                    "selected": 0
                                },
                                "NVP": {
                                    "value": "NVP",
                                    "selected": 0
                                },
                                "PUP": {
                                    "value": "PUP",
                                    "selected": 0
                                },
                                "ARGUS": {
                                    "value": "ARGUS",
                                    "selected": 0
                                },
                                "EMCON": {
                                    "value": "EMCON",
                                    "selected": 0
                                },
                                "XNET": {
                                    "value": "XNET",
                                    "selected": 0
                                },
                                "CHAOS": {
                                    "value": "CHAOS",
                                    "selected": 0
                                },
                                "UDP": {
                                    "value": "UDP",
                                    "selected": 0
                                },
                                "MUX": {
                                    "value": "MUX",
                                    "selected": 0
                                },
                                "DCN": {
                                    "value": "DCN",
                                    "selected": 0
                                },
                                "HMP": {
                                    "value": "HMP",
                                    "selected": 0
                                },
                                "PRM": {
                                    "value": "PRM",
                                    "selected": 0
                                },
                                "XNS-IDP": {
                                    "value": "XNS-IDP",
                                    "selected": 0
                                },
                                "TRUNK-1": {
                                    "value": "TRUNK-1",
                                    "selected": 0
                                },
                                "TRUNK-2": {
                                    "value": "TRUNK-2",
                                    "selected": 0
                                },
                                "LEAF-1": {
                                    "value": "LEAF-1",
                                    "selected": 0
                                },
                                "LEAF-2": {
                                    "value": "LEAF-2",
                                    "selected": 0
                                },
                                "RDP": {
                                    "value": "RDP",
                                    "selected": 0
                                },
                                "IRTP": {
                                    "value": "IRTP",
                                    "selected": 0
                                },
                                "ISO-TP4": {
                                    "value": "ISO-TP4",
                                    "selected": 0
                                },
                                "NETBLT": {
                                    "value": "NETBLT",
                                    "selected": 0
                                },
                                "MFE-NSP": {
                                    "value": "MFE-NSP",
                                    "selected": 0
                                },
                                "MERIT-INP": {
                                    "value": "MERIT-INP",
                                    "selected": 0
                                },
                                "DCCP": {
                                    "value": "DCCP",
                                    "selected": 0
                                },
                                "3PC": {
                                    "value": "3PC",
                                    "selected": 0
                                },
                                "IDPR": {
                                    "value": "IDPR",
                                    "selected": 0
                                },
                                "XTP": {
                                    "value": "XTP",
                                    "selected": 0
                                },
                                "DDP": {
                                    "value": "DDP",
                                    "selected": 0
                                },
                                "IDPR-CMTP": {
                                    "value": "IDPR-CMTP",
                                    "selected": 0
                                },
                                "TP++": {
                                    "value": "TP++",
                                    "selected": 0
                                },
                                "IL": {
                                    "value": "IL",
                                    "selected": 0
                                },
                                "IPV6": {
                                    "value": "IPV6",
                                    "selected": 0
                                },
                                "SDRP": {
                                    "value": "SDRP",
                                    "selected": 0
                                },
                                "IDRP": {
                                    "value": "IDRP",
                                    "selected": 0
                                },
                                "RSVP": {
                                    "value": "RSVP",
                                    "selected": 0
                                },
                                "GRE": {
                                    "value": "GRE",
                                    "selected": 0
                                },
                                "DSR": {
                                    "value": "DSR",
                                    "selected": 0
                                },
                                "BNA": {
                                    "value": "BNA",
                                    "selected": 0
                                },
                                "ESP": {
                                    "value": "ESP",
                                    "selected": 0
                                },
                                "AH": {
                                    "value": "AH",
                                    "selected": 0
                                },
                                "I-NLSP": {
                                    "value": "I-NLSP",
                                    "selected": 0
                                },
                                "SWIPE": {
                                    "value": "SWIPE",
                                    "selected": 0
                                },
                                "NARP": {
                                    "value": "NARP",
                                    "selected": 0
                                },
                                "MOBILE": {
                                    "value": "MOBILE",
                                    "selected": 0
                                },
                                "TLSP": {
                                    "value": "TLSP",
                                    "selected": 0
                                },
                                "SKIP": {
                                    "value": "SKIP",
                                    "selected": 0
                                },
                                "IPV6-ICMP": {
                                    "value": "IPV6-ICMP",
                                    "selected": 0
                                },
                                "CFTP": {
                                    "value": "CFTP",
                                    "selected": 0
                                },
                                "SAT-EXPAK": {
                                    "value": "SAT-EXPAK",
                                    "selected": 0
                                },
                                "KRYPTOLAN": {
                                    "value": "KRYPTOLAN",
                                    "selected": 0
                                },
                                "RVD": {
                                    "value": "RVD",
                                    "selected": 0
                                },
                                "IPPC": {
                                    "value": "IPPC",
                                    "selected": 0
                                },
                                "SAT-MON": {
                                    "value": "SAT-MON",
                                    "selected": 0
                                },
                                "VISA": {
                                    "value": "VISA",
                                    "selected": 0
                                },
                                "IPCV": {
                                    "value": "IPCV",
                                    "selected": 0
                                },
                                "CPNX": {
                                    "value": "CPNX",
                                    "selected": 0
                                },
                                "CPHB": {
                                    "value": "CPHB",
                                    "selected": 0
                                },
                                "WSN": {
                                    "value": "WSN",
                                    "selected": 0
                                },
                                "PVP": {
                                    "value": "PVP",
                                    "selected": 0
                                },
                                "BR-SAT-MON": {
                                    "value": "BR-SAT-MON",
                                    "selected": 0
                                },
                                "SUN-ND": {
                                    "value": "SUN-ND",
                                    "selected": 0
                                },
                                "WB-MON": {
                                    "value": "WB-MON",
                                    "selected": 0
                                },
                                "WB-EXPAK": {
                                    "value": "WB-EXPAK",
                                    "selected": 0
                                },
                                "ISO-IP": {
                                    "value": "ISO-IP",
                                    "selected": 0
                                },
                                "VMTP": {
                                    "value": "VMTP",
                                    "selected": 0
                                },
                                "SECURE-VMTP": {
                                    "value": "SECURE-VMTP",
                                    "selected": 0
                                },
                                "VINES": {
                                    "value": "VINES",
                                    "selected": 0
                                },
                                "TTP": {
                                    "value": "TTP",
                                    "selected": 0
                                },
                                "NSFNET-IGP": {
                                    "value": "NSFNET-IGP",
                                    "selected": 0
                                },
                                "DGP": {
                                    "value": "DGP",
                                    "selected": 0
                                },
                                "TCF": {
                                    "value": "TCF",
                                    "selected": 0
                                },
                                "EIGRP": {
                                    "value": "EIGRP",
                                    "selected": 0
                                },
                                "OSPF": {
                                    "value": "OSPF",
                                    "selected": 0
                                },
                                "SPRITE-RPC": {
                                    "value": "SPRITE-RPC",
                                    "selected": 0
                                },
                                "LARP": {
                                    "value": "LARP",
                                    "selected": 0
                                },
                                "MTP": {
                                    "value": "MTP",
                                    "selected": 0
                                },
                                "AX.25": {
                                    "value": "AX.25",
                                    "selected": 0
                                },
                                "IPIP": {
                                    "value": "IPIP",
                                    "selected": 0
                                },
                                "MICP": {
                                    "value": "MICP",
                                    "selected": 0
                                },
                                "SCC-SP": {
                                    "value": "SCC-SP",
                                    "selected": 0
                                },
                                "ETHERIP": {
                                    "value": "ETHERIP",
                                    "selected": 0
                                },
                                "ENCAP": {
                                    "value": "ENCAP",
                                    "selected": 0
                                },
                                "GMTP": {
                                    "value": "GMTP",
                                    "selected": 0
                                },
                                "IFMP": {
                                    "value": "IFMP",
                                    "selected": 0
                                },
                                "PNNI": {
                                    "value": "PNNI",
                                    "selected": 0
                                },
                                "PIM": {
                                    "value": "PIM",
                                    "selected": 0
                                },
                                "ARIS": {
                                    "value": "ARIS",
                                    "selected": 0
                                },
                                "SCPS": {
                                    "value": "SCPS",
                                    "selected": 0
                                },
                                "QNX": {
                                    "value": "QNX",
                                    "selected": 0
                                },
                                "A/N": {
                                    "value": "A/N",
                                    "selected": 0
                                },
                                "IPCOMP": {
                                    "value": "IPCOMP",
                                    "selected": 0
                                },
                                "SNP": {
                                    "value": "SNP",
                                    "selected": 0
                                },
                                "COMPAQ-PEER": {
                                    "value": "COMPAQ-PEER",
                                    "selected": 0
                                },
                                "IPX-IN-IP": {
                                    "value": "IPX-IN-IP",
                                    "selected": 0
                                },
                                "CARP": {
                                    "value": "CARP",
                                    "selected": 0
                                },
                                "PGM": {
                                    "value": "PGM",
                                    "selected": 0
                                },
                                "L2TP": {
                                    "value": "L2TP",
                                    "selected": 0
                                },
                                "DDX": {
                                    "value": "DDX",
                                    "selected": 0
                                },
                                "IATP": {
                                    "value": "IATP",
                                    "selected": 0
                                },
                                "STP": {
                                    "value": "STP",
                                    "selected": 0
                                },
                                "SRP": {
                                    "value": "SRP",
                                    "selected": 0
                                },
                                "UTI": {
                                    "value": "UTI",
                                    "selected": 0
                                },
                                "SMP": {
                                    "value": "SMP",
                                    "selected": 0
                                },
                                "SM": {
                                    "value": "SM",
                                    "selected": 0
                                },
                                "PTP": {
                                    "value": "PTP",
                                    "selected": 0
                                },
                                "ISIS": {
                                    "value": "ISIS",
                                    "selected": 0
                                },
                                "CRTP": {
                                    "value": "CRTP",
                                    "selected": 0
                                },
                                "CRUDP": {
                                    "value": "CRUDP",
                                    "selected": 0
                                },
                                "SPS": {
                                    "value": "SPS",
                                    "selected": 0
                                },
                                "PIPE": {
                                    "value": "PIPE",
                                    "selected": 0
                                },
                                "SCTP": {
                                    "value": "SCTP",
                                    "selected": 0
                                },
                                "FC": {
                                    "value": "FC",
                                    "selected": 0
                                },
                                "RSVP-E2E-IGNORE": {
                                    "value": "RSVP-E2E-IGNORE",
                                    "selected": 0
                                },
                                "UDPLITE": {
                                    "value": "UDPLITE",
                                    "selected": 0
                                },
                                "MPLS-IN-IP": {
                                    "value": "MPLS-IN-IP",
                                    "selected": 0
                                },
                                "MANET": {
                                    "value": "MANET",
                                    "selected": 0
                                },
                                "HIP": {
                                    "value": "HIP",
                                    "selected": 0
                                },
                                "SHIM6": {
                                    "value": "SHIM6",
                                    "selected": 0
                                },
                                "WESP": {
                                    "value": "WESP",
                                    "selected": 0
                                },
                                "ROHC": {
                                    "value": "ROHC",
                                    "selected": 0
                                },
                                "PFSYNC": {
                                    "value": "PFSYNC",
                                    "selected": 0
                                },
                                "DIVERT": {
                                    "value": "DIVERT",
                                    "selected": 0
                                }
                            },
                            "source_net": "10.0.0.0/24",
                            "source_not": "0",
                            "source_port": "80",
                            "destination_net": "192.168.0.0/24",
                            "destination_not": "0",
                            "destination_port": "http",
                            "gateway": {
                                "": {
                                    "value": "none",
                                    "selected": True
                                },
                                "Null4": {
                                    "value": "Null4 - 127.0.0.1",
                                    "selected": 0
                                },
                                "Null6": {
                                    "value": "Null6 - ::1",
                                    "selected": 0
                                },
                                "WAN_DHCP": {
                                    "value": "WAN_DHCP - 10.0.2.2",
                                    "selected": 0
                                },
                                "WAN_DHCP6": {
                                    "value": "WAN_DHCP6 - inet6",
                                    "selected": 0
                                }
                            },
                            "log": "0",
                            "description": "test Rule astuerz"
                        },
                        "fb0e1f6c-9f39-46dd-9c98-27fc314a2429": {
                            "enabled": "1",
                            "sequence": "5",
                            "action": {
                                "pass": {
                                    "value": "Pass",
                                    "selected": 1
                                },
                                "block": {
                                    "value": "Block",
                                    "selected": 0
                                },
                                "reject": {
                                    "value": "Reject",
                                    "selected": 0
                                }
                            },
                            "quick": "1",
                            "interface": {
                                "lan": {
                                    "value": "LAN",
                                    "selected": 1
                                },
                                "lo0": {
                                    "value": "Loopback",
                                    "selected": 0
                                },
                                "wan": {
                                    "value": "WAN",
                                    "selected": 0
                                }
                            },
                            "direction": {
                                "in": {
                                    "value": "In",
                                    "selected": 1
                                },
                                "out": {
                                    "value": "Out",
                                    "selected": 0
                                }
                            },
                            "ipprotocol": {
                                "inet": {
                                    "value": "IPv4",
                                    "selected": 1
                                },
                                "inet6": {
                                    "value": "IPv6",
                                    "selected": 0
                                }
                            },
                            "protocol": {
                                "any": {
                                    "value": "any",
                                    "selected": 0
                                },
                                "ICMP": {
                                    "value": "ICMP",
                                    "selected": 0
                                },
                                "IGMP": {
                                    "value": "IGMP",
                                    "selected": 0
                                },
                                "GGP": {
                                    "value": "GGP",
                                    "selected": 0
                                },
                                "IPENCAP": {
                                    "value": "IPENCAP",
                                    "selected": 0
                                },
                                "ST2": {
                                    "value": "ST2",
                                    "selected": 0
                                },
                                "TCP": {
                                    "value": "TCP",
                                    "selected": 1
                                },
                                "CBT": {
                                    "value": "CBT",
                                    "selected": 0
                                },
                                "EGP": {
                                    "value": "EGP",
                                    "selected": 0
                                },
                                "IGP": {
                                    "value": "IGP",
                                    "selected": 0
                                },
                                "BBN-RCC": {
                                    "value": "BBN-RCC",
                                    "selected": 0
                                },
                                "NVP": {
                                    "value": "NVP",
                                    "selected": 0
                                },
                                "PUP": {
                                    "value": "PUP",
                                    "selected": 0
                                },
                                "ARGUS": {
                                    "value": "ARGUS",
                                    "selected": 0
                                },
                                "EMCON": {
                                    "value": "EMCON",
                                    "selected": 0
                                },
                                "XNET": {
                                    "value": "XNET",
                                    "selected": 0
                                },
                                "CHAOS": {
                                    "value": "CHAOS",
                                    "selected": 0
                                },
                                "UDP": {
                                    "value": "UDP",
                                    "selected": 0
                                },
                                "MUX": {
                                    "value": "MUX",
                                    "selected": 0
                                },
                                "DCN": {
                                    "value": "DCN",
                                    "selected": 0
                                },
                                "HMP": {
                                    "value": "HMP",
                                    "selected": 0
                                },
                                "PRM": {
                                    "value": "PRM",
                                    "selected": 0
                                },
                                "XNS-IDP": {
                                    "value": "XNS-IDP",
                                    "selected": 0
                                },
                                "TRUNK-1": {
                                    "value": "TRUNK-1",
                                    "selected": 0
                                },
                                "TRUNK-2": {
                                    "value": "TRUNK-2",
                                    "selected": 0
                                },
                                "LEAF-1": {
                                    "value": "LEAF-1",
                                    "selected": 0
                                },
                                "LEAF-2": {
                                    "value": "LEAF-2",
                                    "selected": 0
                                },
                                "RDP": {
                                    "value": "RDP",
                                    "selected": 0
                                },
                                "IRTP": {
                                    "value": "IRTP",
                                    "selected": 0
                                },
                                "ISO-TP4": {
                                    "value": "ISO-TP4",
                                    "selected": 0
                                },
                                "NETBLT": {
                                    "value": "NETBLT",
                                    "selected": 0
                                },
                                "MFE-NSP": {
                                    "value": "MFE-NSP",
                                    "selected": 0
                                },
                                "MERIT-INP": {
                                    "value": "MERIT-INP",
                                    "selected": 0
                                },
                                "DCCP": {
                                    "value": "DCCP",
                                    "selected": 0
                                },
                                "3PC": {
                                    "value": "3PC",
                                    "selected": 0
                                },
                                "IDPR": {
                                    "value": "IDPR",
                                    "selected": 0
                                },
                                "XTP": {
                                    "value": "XTP",
                                    "selected": 0
                                },
                                "DDP": {
                                    "value": "DDP",
                                    "selected": 0
                                },
                                "IDPR-CMTP": {
                                    "value": "IDPR-CMTP",
                                    "selected": 0
                                },
                                "TP++": {
                                    "value": "TP++",
                                    "selected": 0
                                },
                                "IL": {
                                    "value": "IL",
                                    "selected": 0
                                },
                                "IPV6": {
                                    "value": "IPV6",
                                    "selected": 0
                                },
                                "SDRP": {
                                    "value": "SDRP",
                                    "selected": 0
                                },
                                "IDRP": {
                                    "value": "IDRP",
                                    "selected": 0
                                },
                                "RSVP": {
                                    "value": "RSVP",
                                    "selected": 0
                                },
                                "GRE": {
                                    "value": "GRE",
                                    "selected": 0
                                },
                                "DSR": {
                                    "value": "DSR",
                                    "selected": 0
                                },
                                "BNA": {
                                    "value": "BNA",
                                    "selected": 0
                                },
                                "ESP": {
                                    "value": "ESP",
                                    "selected": 0
                                },
                                "AH": {
                                    "value": "AH",
                                    "selected": 0
                                },
                                "I-NLSP": {
                                    "value": "I-NLSP",
                                    "selected": 0
                                },
                                "SWIPE": {
                                    "value": "SWIPE",
                                    "selected": 0
                                },
                                "NARP": {
                                    "value": "NARP",
                                    "selected": 0
                                },
                                "MOBILE": {
                                    "value": "MOBILE",
                                    "selected": 0
                                },
                                "TLSP": {
                                    "value": "TLSP",
                                    "selected": 0
                                },
                                "SKIP": {
                                    "value": "SKIP",
                                    "selected": 0
                                },
                                "IPV6-ICMP": {
                                    "value": "IPV6-ICMP",
                                    "selected": 0
                                },
                                "CFTP": {
                                    "value": "CFTP",
                                    "selected": 0
                                },
                                "SAT-EXPAK": {
                                    "value": "SAT-EXPAK",
                                    "selected": 0
                                },
                                "KRYPTOLAN": {
                                    "value": "KRYPTOLAN",
                                    "selected": 0
                                },
                                "RVD": {
                                    "value": "RVD",
                                    "selected": 0
                                },
                                "IPPC": {
                                    "value": "IPPC",
                                    "selected": 0
                                },
                                "SAT-MON": {
                                    "value": "SAT-MON",
                                    "selected": 0
                                },
                                "VISA": {
                                    "value": "VISA",
                                    "selected": 0
                                },
                                "IPCV": {
                                    "value": "IPCV",
                                    "selected": 0
                                },
                                "CPNX": {
                                    "value": "CPNX",
                                    "selected": 0
                                },
                                "CPHB": {
                                    "value": "CPHB",
                                    "selected": 0
                                },
                                "WSN": {
                                    "value": "WSN",
                                    "selected": 0
                                },
                                "PVP": {
                                    "value": "PVP",
                                    "selected": 0
                                },
                                "BR-SAT-MON": {
                                    "value": "BR-SAT-MON",
                                    "selected": 0
                                },
                                "SUN-ND": {
                                    "value": "SUN-ND",
                                    "selected": 0
                                },
                                "WB-MON": {
                                    "value": "WB-MON",
                                    "selected": 0
                                },
                                "WB-EXPAK": {
                                    "value": "WB-EXPAK",
                                    "selected": 0
                                },
                                "ISO-IP": {
                                    "value": "ISO-IP",
                                    "selected": 0
                                },
                                "VMTP": {
                                    "value": "VMTP",
                                    "selected": 0
                                },
                                "SECURE-VMTP": {
                                    "value": "SECURE-VMTP",
                                    "selected": 0
                                },
                                "VINES": {
                                    "value": "VINES",
                                    "selected": 0
                                },
                                "TTP": {
                                    "value": "TTP",
                                    "selected": 0
                                },
                                "NSFNET-IGP": {
                                    "value": "NSFNET-IGP",
                                    "selected": 0
                                },
                                "DGP": {
                                    "value": "DGP",
                                    "selected": 0
                                },
                                "TCF": {
                                    "value": "TCF",
                                    "selected": 0
                                },
                                "EIGRP": {
                                    "value": "EIGRP",
                                    "selected": 0
                                },
                                "OSPF": {
                                    "value": "OSPF",
                                    "selected": 0
                                },
                                "SPRITE-RPC": {
                                    "value": "SPRITE-RPC",
                                    "selected": 0
                                },
                                "LARP": {
                                    "value": "LARP",
                                    "selected": 0
                                },
                                "MTP": {
                                    "value": "MTP",
                                    "selected": 0
                                },
                                "AX.25": {
                                    "value": "AX.25",
                                    "selected": 0
                                },
                                "IPIP": {
                                    "value": "IPIP",
                                    "selected": 0
                                },
                                "MICP": {
                                    "value": "MICP",
                                    "selected": 0
                                },
                                "SCC-SP": {
                                    "value": "SCC-SP",
                                    "selected": 0
                                },
                                "ETHERIP": {
                                    "value": "ETHERIP",
                                    "selected": 0
                                },
                                "ENCAP": {
                                    "value": "ENCAP",
                                    "selected": 0
                                },
                                "GMTP": {
                                    "value": "GMTP",
                                    "selected": 0
                                },
                                "IFMP": {
                                    "value": "IFMP",
                                    "selected": 0
                                },
                                "PNNI": {
                                    "value": "PNNI",
                                    "selected": 0
                                },
                                "PIM": {
                                    "value": "PIM",
                                    "selected": 0
                                },
                                "ARIS": {
                                    "value": "ARIS",
                                    "selected": 0
                                },
                                "SCPS": {
                                    "value": "SCPS",
                                    "selected": 0
                                },
                                "QNX": {
                                    "value": "QNX",
                                    "selected": 0
                                },
                                "A/N": {
                                    "value": "A/N",
                                    "selected": 0
                                },
                                "IPCOMP": {
                                    "value": "IPCOMP",
                                    "selected": 0
                                },
                                "SNP": {
                                    "value": "SNP",
                                    "selected": 0
                                },
                                "COMPAQ-PEER": {
                                    "value": "COMPAQ-PEER",
                                    "selected": 0
                                },
                                "IPX-IN-IP": {
                                    "value": "IPX-IN-IP",
                                    "selected": 0
                                },
                                "CARP": {
                                    "value": "CARP",
                                    "selected": 0
                                },
                                "PGM": {
                                    "value": "PGM",
                                    "selected": 0
                                },
                                "L2TP": {
                                    "value": "L2TP",
                                    "selected": 0
                                },
                                "DDX": {
                                    "value": "DDX",
                                    "selected": 0
                                },
                                "IATP": {
                                    "value": "IATP",
                                    "selected": 0
                                },
                                "STP": {
                                    "value": "STP",
                                    "selected": 0
                                },
                                "SRP": {
                                    "value": "SRP",
                                    "selected": 0
                                },
                                "UTI": {
                                    "value": "UTI",
                                    "selected": 0
                                },
                                "SMP": {
                                    "value": "SMP",
                                    "selected": 0
                                },
                                "SM": {
                                    "value": "SM",
                                    "selected": 0
                                },
                                "PTP": {
                                    "value": "PTP",
                                    "selected": 0
                                },
                                "ISIS": {
                                    "value": "ISIS",
                                    "selected": 0
                                },
                                "CRTP": {
                                    "value": "CRTP",
                                    "selected": 0
                                },
                                "CRUDP": {
                                    "value": "CRUDP",
                                    "selected": 0
                                },
                                "SPS": {
                                    "value": "SPS",
                                    "selected": 0
                                },
                                "PIPE": {
                                    "value": "PIPE",
                                    "selected": 0
                                },
                                "SCTP": {
                                    "value": "SCTP",
                                    "selected": 0
                                },
                                "FC": {
                                    "value": "FC",
                                    "selected": 0
                                },
                                "RSVP-E2E-IGNORE": {
                                    "value": "RSVP-E2E-IGNORE",
                                    "selected": 0
                                },
                                "UDPLITE": {
                                    "value": "UDPLITE",
                                    "selected": 0
                                },
                                "MPLS-IN-IP": {
                                    "value": "MPLS-IN-IP",
                                    "selected": 0
                                },
                                "MANET": {
                                    "value": "MANET",
                                    "selected": 0
                                },
                                "HIP": {
                                    "value": "HIP",
                                    "selected": 0
                                },
                                "SHIM6": {
                                    "value": "SHIM6",
                                    "selected": 0
                                },
                                "WESP": {
                                    "value": "WESP",
                                    "selected": 0
                                },
                                "ROHC": {
                                    "value": "ROHC",
                                    "selected": 0
                                },
                                "PFSYNC": {
                                    "value": "PFSYNC",
                                    "selected": 0
                                },
                                "DIVERT": {
                                    "value": "DIVERT",
                                    "selected": 0
                                }
                            },
                            "source_net": "my_alias",
                            "source_not": "0",
                            "source_port": "",
                            "destination_net": "my_alias",
                            "destination_not": "0",
                            "destination_port": "http",
                            "gateway": {
                                "": {
                                    "value": "none",
                                    "selected": True
                                },
                                "Null4": {
                                    "value": "Null4 - 127.0.0.1",
                                    "selected": 0
                                },
                                "Null6": {
                                    "value": "Null6 - ::1",
                                    "selected": 0
                                },
                                "WAN_DHCP": {
                                    "value": "WAN_DHCP - 10.0.2.2",
                                    "selected": 0
                                },
                                "WAN_DHCP6": {
                                    "value": "WAN_DHCP6 - inet6",
                                    "selected": 0
                                }
                            },
                            "log": "0",
                            "description": "test Rule with alias"
                        },
                        "39d68aa9-b7cd-40ab-b4c3-1c1c36a3a367": {
                            "enabled": "1",
                            "sequence": "10",
                            "action": {
                                "pass": {
                                    "value": "Pass",
                                    "selected": 1
                                },
                                "block": {
                                    "value": "Block",
                                    "selected": 0
                                },
                                "reject": {
                                    "value": "Reject",
                                    "selected": 0
                                }
                            },
                            "quick": "1",
                            "interface": {
                                "lan": {
                                    "value": "LAN",
                                    "selected": 1
                                },
                                "lo0": {
                                    "value": "Loopback",
                                    "selected": 0
                                },
                                "wan": {
                                    "value": "WAN",
                                    "selected": 0
                                }
                            },
                            "direction": {
                                "in": {
                                    "value": "In",
                                    "selected": 1
                                },
                                "out": {
                                    "value": "Out",
                                    "selected": 0
                                }
                            },
                            "ipprotocol": {
                                "inet": {
                                    "value": "IPv4",
                                    "selected": 1
                                },
                                "inet6": {
                                    "value": "IPv6",
                                    "selected": 0
                                }
                            },
                            "protocol": {
                                "any": {
                                    "value": "any",
                                    "selected": 0
                                },
                                "ICMP": {
                                    "value": "ICMP",
                                    "selected": 0
                                },
                                "IGMP": {
                                    "value": "IGMP",
                                    "selected": 0
                                },
                                "GGP": {
                                    "value": "GGP",
                                    "selected": 0
                                },
                                "IPENCAP": {
                                    "value": "IPENCAP",
                                    "selected": 0
                                },
                                "ST2": {
                                    "value": "ST2",
                                    "selected": 0
                                },
                                "TCP": {
                                    "value": "TCP",
                                    "selected": 1
                                },
                                "CBT": {
                                    "value": "CBT",
                                    "selected": 0
                                },
                                "EGP": {
                                    "value": "EGP",
                                    "selected": 0
                                },
                                "IGP": {
                                    "value": "IGP",
                                    "selected": 0
                                },
                                "BBN-RCC": {
                                    "value": "BBN-RCC",
                                    "selected": 0
                                },
                                "NVP": {
                                    "value": "NVP",
                                    "selected": 0
                                },
                                "PUP": {
                                    "value": "PUP",
                                    "selected": 0
                                },
                                "ARGUS": {
                                    "value": "ARGUS",
                                    "selected": 0
                                },
                                "EMCON": {
                                    "value": "EMCON",
                                    "selected": 0
                                },
                                "XNET": {
                                    "value": "XNET",
                                    "selected": 0
                                },
                                "CHAOS": {
                                    "value": "CHAOS",
                                    "selected": 0
                                },
                                "UDP": {
                                    "value": "UDP",
                                    "selected": 0
                                },
                                "MUX": {
                                    "value": "MUX",
                                    "selected": 0
                                },
                                "DCN": {
                                    "value": "DCN",
                                    "selected": 0
                                },
                                "HMP": {
                                    "value": "HMP",
                                    "selected": 0
                                },
                                "PRM": {
                                    "value": "PRM",
                                    "selected": 0
                                },
                                "XNS-IDP": {
                                    "value": "XNS-IDP",
                                    "selected": 0
                                },
                                "TRUNK-1": {
                                    "value": "TRUNK-1",
                                    "selected": 0
                                },
                                "TRUNK-2": {
                                    "value": "TRUNK-2",
                                    "selected": 0
                                },
                                "LEAF-1": {
                                    "value": "LEAF-1",
                                    "selected": 0
                                },
                                "LEAF-2": {
                                    "value": "LEAF-2",
                                    "selected": 0
                                },
                                "RDP": {
                                    "value": "RDP",
                                    "selected": 0
                                },
                                "IRTP": {
                                    "value": "IRTP",
                                    "selected": 0
                                },
                                "ISO-TP4": {
                                    "value": "ISO-TP4",
                                    "selected": 0
                                },
                                "NETBLT": {
                                    "value": "NETBLT",
                                    "selected": 0
                                },
                                "MFE-NSP": {
                                    "value": "MFE-NSP",
                                    "selected": 0
                                },
                                "MERIT-INP": {
                                    "value": "MERIT-INP",
                                    "selected": 0
                                },
                                "DCCP": {
                                    "value": "DCCP",
                                    "selected": 0
                                },
                                "3PC": {
                                    "value": "3PC",
                                    "selected": 0
                                },
                                "IDPR": {
                                    "value": "IDPR",
                                    "selected": 0
                                },
                                "XTP": {
                                    "value": "XTP",
                                    "selected": 0
                                },
                                "DDP": {
                                    "value": "DDP",
                                    "selected": 0
                                },
                                "IDPR-CMTP": {
                                    "value": "IDPR-CMTP",
                                    "selected": 0
                                },
                                "TP++": {
                                    "value": "TP++",
                                    "selected": 0
                                },
                                "IL": {
                                    "value": "IL",
                                    "selected": 0
                                },
                                "IPV6": {
                                    "value": "IPV6",
                                    "selected": 0
                                },
                                "SDRP": {
                                    "value": "SDRP",
                                    "selected": 0
                                },
                                "IDRP": {
                                    "value": "IDRP",
                                    "selected": 0
                                },
                                "RSVP": {
                                    "value": "RSVP",
                                    "selected": 0
                                },
                                "GRE": {
                                    "value": "GRE",
                                    "selected": 0
                                },
                                "DSR": {
                                    "value": "DSR",
                                    "selected": 0
                                },
                                "BNA": {
                                    "value": "BNA",
                                    "selected": 0
                                },
                                "ESP": {
                                    "value": "ESP",
                                    "selected": 0
                                },
                                "AH": {
                                    "value": "AH",
                                    "selected": 0
                                },
                                "I-NLSP": {
                                    "value": "I-NLSP",
                                    "selected": 0
                                },
                                "SWIPE": {
                                    "value": "SWIPE",
                                    "selected": 0
                                },
                                "NARP": {
                                    "value": "NARP",
                                    "selected": 0
                                },
                                "MOBILE": {
                                    "value": "MOBILE",
                                    "selected": 0
                                },
                                "TLSP": {
                                    "value": "TLSP",
                                    "selected": 0
                                },
                                "SKIP": {
                                    "value": "SKIP",
                                    "selected": 0
                                },
                                "IPV6-ICMP": {
                                    "value": "IPV6-ICMP",
                                    "selected": 0
                                },
                                "CFTP": {
                                    "value": "CFTP",
                                    "selected": 0
                                },
                                "SAT-EXPAK": {
                                    "value": "SAT-EXPAK",
                                    "selected": 0
                                },
                                "KRYPTOLAN": {
                                    "value": "KRYPTOLAN",
                                    "selected": 0
                                },
                                "RVD": {
                                    "value": "RVD",
                                    "selected": 0
                                },
                                "IPPC": {
                                    "value": "IPPC",
                                    "selected": 0
                                },
                                "SAT-MON": {
                                    "value": "SAT-MON",
                                    "selected": 0
                                },
                                "VISA": {
                                    "value": "VISA",
                                    "selected": 0
                                },
                                "IPCV": {
                                    "value": "IPCV",
                                    "selected": 0
                                },
                                "CPNX": {
                                    "value": "CPNX",
                                    "selected": 0
                                },
                                "CPHB": {
                                    "value": "CPHB",
                                    "selected": 0
                                },
                                "WSN": {
                                    "value": "WSN",
                                    "selected": 0
                                },
                                "PVP": {
                                    "value": "PVP",
                                    "selected": 0
                                },
                                "BR-SAT-MON": {
                                    "value": "BR-SAT-MON",
                                    "selected": 0
                                },
                                "SUN-ND": {
                                    "value": "SUN-ND",
                                    "selected": 0
                                },
                                "WB-MON": {
                                    "value": "WB-MON",
                                    "selected": 0
                                },
                                "WB-EXPAK": {
                                    "value": "WB-EXPAK",
                                    "selected": 0
                                },
                                "ISO-IP": {
                                    "value": "ISO-IP",
                                    "selected": 0
                                },
                                "VMTP": {
                                    "value": "VMTP",
                                    "selected": 0
                                },
                                "SECURE-VMTP": {
                                    "value": "SECURE-VMTP",
                                    "selected": 0
                                },
                                "VINES": {
                                    "value": "VINES",
                                    "selected": 0
                                },
                                "TTP": {
                                    "value": "TTP",
                                    "selected": 0
                                },
                                "NSFNET-IGP": {
                                    "value": "NSFNET-IGP",
                                    "selected": 0
                                },
                                "DGP": {
                                    "value": "DGP",
                                    "selected": 0
                                },
                                "TCF": {
                                    "value": "TCF",
                                    "selected": 0
                                },
                                "EIGRP": {
                                    "value": "EIGRP",
                                    "selected": 0
                                },
                                "OSPF": {
                                    "value": "OSPF",
                                    "selected": 0
                                },
                                "SPRITE-RPC": {
                                    "value": "SPRITE-RPC",
                                    "selected": 0
                                },
                                "LARP": {
                                    "value": "LARP",
                                    "selected": 0
                                },
                                "MTP": {
                                    "value": "MTP",
                                    "selected": 0
                                },
                                "AX.25": {
                                    "value": "AX.25",
                                    "selected": 0
                                },
                                "IPIP": {
                                    "value": "IPIP",
                                    "selected": 0
                                },
                                "MICP": {
                                    "value": "MICP",
                                    "selected": 0
                                },
                                "SCC-SP": {
                                    "value": "SCC-SP",
                                    "selected": 0
                                },
                                "ETHERIP": {
                                    "value": "ETHERIP",
                                    "selected": 0
                                },
                                "ENCAP": {
                                    "value": "ENCAP",
                                    "selected": 0
                                },
                                "GMTP": {
                                    "value": "GMTP",
                                    "selected": 0
                                },
                                "IFMP": {
                                    "value": "IFMP",
                                    "selected": 0
                                },
                                "PNNI": {
                                    "value": "PNNI",
                                    "selected": 0
                                },
                                "PIM": {
                                    "value": "PIM",
                                    "selected": 0
                                },
                                "ARIS": {
                                    "value": "ARIS",
                                    "selected": 0
                                },
                                "SCPS": {
                                    "value": "SCPS",
                                    "selected": 0
                                },
                                "QNX": {
                                    "value": "QNX",
                                    "selected": 0
                                },
                                "A/N": {
                                    "value": "A/N",
                                    "selected": 0
                                },
                                "IPCOMP": {
                                    "value": "IPCOMP",
                                    "selected": 0
                                },
                                "SNP": {
                                    "value": "SNP",
                                    "selected": 0
                                },
                                "COMPAQ-PEER": {
                                    "value": "COMPAQ-PEER",
                                    "selected": 0
                                },
                                "IPX-IN-IP": {
                                    "value": "IPX-IN-IP",
                                    "selected": 0
                                },
                                "CARP": {
                                    "value": "CARP",
                                    "selected": 0
                                },
                                "PGM": {
                                    "value": "PGM",
                                    "selected": 0
                                },
                                "L2TP": {
                                    "value": "L2TP",
                                    "selected": 0
                                },
                                "DDX": {
                                    "value": "DDX",
                                    "selected": 0
                                },
                                "IATP": {
                                    "value": "IATP",
                                    "selected": 0
                                },
                                "STP": {
                                    "value": "STP",
                                    "selected": 0
                                },
                                "SRP": {
                                    "value": "SRP",
                                    "selected": 0
                                },
                                "UTI": {
                                    "value": "UTI",
                                    "selected": 0
                                },
                                "SMP": {
                                    "value": "SMP",
                                    "selected": 0
                                },
                                "SM": {
                                    "value": "SM",
                                    "selected": 0
                                },
                                "PTP": {
                                    "value": "PTP",
                                    "selected": 0
                                },
                                "ISIS": {
                                    "value": "ISIS",
                                    "selected": 0
                                },
                                "CRTP": {
                                    "value": "CRTP",
                                    "selected": 0
                                },
                                "CRUDP": {
                                    "value": "CRUDP",
                                    "selected": 0
                                },
                                "SPS": {
                                    "value": "SPS",
                                    "selected": 0
                                },
                                "PIPE": {
                                    "value": "PIPE",
                                    "selected": 0
                                },
                                "SCTP": {
                                    "value": "SCTP",
                                    "selected": 0
                                },
                                "FC": {
                                    "value": "FC",
                                    "selected": 0
                                },
                                "RSVP-E2E-IGNORE": {
                                    "value": "RSVP-E2E-IGNORE",
                                    "selected": 0
                                },
                                "UDPLITE": {
                                    "value": "UDPLITE",
                                    "selected": 0
                                },
                                "MPLS-IN-IP": {
                                    "value": "MPLS-IN-IP",
                                    "selected": 0
                                },
                                "MANET": {
                                    "value": "MANET",
                                    "selected": 0
                                },
                                "HIP": {
                                    "value": "HIP",
                                    "selected": 0
                                },
                                "SHIM6": {
                                    "value": "SHIM6",
                                    "selected": 0
                                },
                                "WESP": {
                                    "value": "WESP",
                                    "selected": 0
                                },
                                "ROHC": {
                                    "value": "ROHC",
                                    "selected": 0
                                },
                                "PFSYNC": {
                                    "value": "PFSYNC",
                                    "selected": 0
                                },
                                "DIVERT": {
                                    "value": "DIVERT",
                                    "selected": 0
                                }
                            },
                            "source_net": "192.168.1.0/24",
                            "source_not": "0",
                            "source_port": "",
                            "destination_net": "10.0.0.0/24",
                            "destination_not": "0",
                            "destination_port": "ftp",
                            "gateway": {
                                "": {
                                    "value": "none",
                                    "selected": True
                                },
                                "Null4": {
                                    "value": "Null4 - 127.0.0.1",
                                    "selected": 0
                                },
                                "Null6": {
                                    "value": "Null6 - ::1",
                                    "selected": 0
                                },
                                "WAN_DHCP": {
                                    "value": "WAN_DHCP - 10.0.2.2",
                                    "selected": 0
                                },
                                "WAN_DHCP6": {
                                    "value": "WAN_DHCP6 - inet6",
                                    "selected": 0
                                }
                            },
                            "log": "0",
                            "description": "Pass rule"
                        }
                    }
                },
                "snatrules": {
                    "rule": []
                }
            }
        }
        self._api_client_args_fixtures = [
            'api_key',
            'api_secret',
            'https://127.0.0.1/api',
            True,
            '~/.opn-cli/ca.pem',
            60
        ]

    @patch('opnsense_cli.commands.plugin.firewall.rule.ApiClient.execute')
    def test_list(self, api_response_mock: Mock):
        columns = (
            'sequence,interface,action,direction,ipprotocol,protocol,'
            'source_net,source_port,destination_net,destination_port'
        )
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            rule,
            ['list', '-c', columns, '-o', 'plain']
        )

        self.assertIn(
            (
                "1 lan pass in inet TCP 10.0.0.0/24 80 192.168.0.0/24 http\n"
                "5 lan pass in inet TCP my_alias  my_alias http\n"
                "10 lan pass in inet TCP 192.168.1.0/24  10.0.0.0/24 ftp\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.plugin.firewall.rule.ApiClient.execute')
    def test_show_NOT_FOUND(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                []
            ],
            rule,
            ['show', 'b468c719-89db-45a8-bd02-b081246dc002']
        )
        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.plugin.firewall.rule.ApiClient.execute')
    def test_show_EMPTY_STRING(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [],
            rule,
            ['show', '']
        )
        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.plugin.firewall.rule.ApiClient.execute')
    def test_show(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                {
                    "rule":
                        self._api_data_fixtures_list['filter']['rules']['rule']['b468c719-89db-45a8-bd02-b081246dc002']
                },
            ],
            rule,
            ['show', 'b468c719-89db-45a8-bd02-b081246dc002', '-o', 'yaml']
        )

        self.assertIn(
            (
                "sequence: '1'\n"
                "action: pass\n"
                "quick: '1'\n"
                "interface: lan\n"
                "direction: in\n"
                "ipprotocol: inet\n"
                "protocol: TCP\n"
                "source_net: 10.0.0.0/24\n"
                "source_not: '0'\n"
                "source_port: '80'\n"
                "destination_net: 192.168.0.0/24\n"
                "destination_not: '0'\n"
                "destination_port: http\n"
                "gateway: ''\n"
                "log: '0'\n"
                "description: test Rule astuerz\n"
                "enabled: '1'\n\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.plugin.firewall.rule.ApiClient.execute')
    def test_create_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_savepoint_OK,
                self._api_data_fixtures_create_OK,
                self._api_data_fixtures_apply_OK,
                self._api_data_fixtures_cancel_rollback_OK,
            ],
            rule,
            [
                "create", "20",
                "-a", "block",
                "--no-quick",
                "-i", "lan,wan",
                "-d", "in",
                "-ip", "inet",
                "-p", "TCP",
                "-src", "20.82.65.183",
                "--no-source-invert",
                "-src-port", "8081",
                "-dst", "192.168.1.1",
                "--no-destination-invert",
                "-dst-port", "https",
                "--gateway", "Null4",
                "--log",
                "-d", "example block rule",
                "--disabled",
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.plugin.firewall.rule.ApiClient.execute')
    def test_create_ERROR(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_savepoint_OK,
                self._api_data_fixtures_create_ERROR,
                self._api_data_fixtures_apply_OK,
                self._api_data_fixtures_cancel_rollback_OK,
            ],
            rule,
            [
                "create", "40",
                "-a", "pass",
                "-i", "lan",
                "-src", "alias_not_exists",
                "-dst", "192.168.1.1",
                "-d", "example fails",
            ]
        )

        self.assertIn(
            (
                "Error: {'result': 'failed', "
                "'validations': {'rule.source_net': 'alias_not_exists is not a valid source IP address or alias.'}}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.plugin.firewall.rule.ApiClient.execute')
    def test_update_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_savepoint_OK,
                self._api_data_fixtures_update_OK,
                self._api_data_fixtures_apply_OK,
                self._api_data_fixtures_cancel_rollback_OK,
            ],
            rule,
            [
                "update", "85282721-934c-42be-ba4d-a93cbfda26af",
                "-s", "7",
                "-a", "pass",
                "--quick",
                "-i", "lan",
                "-d", "out",
                "-ip", "inet",
                "-p", "TCP",
                "-src", "example_alias",
                "--source-invert",
                "-src-port", "",
                "-dst", "20.82.65.183",
                "--destination-invert",
                "-dst-port", "ssh",
                "--gateway", "",
                "--no-log",
                "-d", "example pass rule",
                "--enabled",
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.plugin.firewall.rule.ApiClient.execute')
    def test_update_NOT_EXISTS(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_savepoint_OK,
                self._api_data_fixtures_update_NOT_EXISTS,
            ],
            rule,
            [
                "update", "85282721-934c-42be-ba4d-a93cbfda26af",
                "--disabled",
            ]
        )

        self.assertIn(
            (
                "Error: {'result': 'failed'}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.plugin.firewall.rule.ApiClient.execute')
    def test_delete_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_savepoint_OK,
                self._api_data_fixtures_delete_OK,
                self._api_data_fixtures_apply_OK,
                self._api_data_fixtures_cancel_rollback_OK,
            ],
            rule,
            [
                "delete", "85282721-934c-42be-ba4d-a93cbfda26af",
            ]
        )

        self.assertIn(
            (
                "deleted \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.plugin.firewall.rule.ApiClient.execute')
    def test_delete_NOT_FOUND(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_savepoint_OK,
                self._api_data_fixtures_delete_NOT_FOUND,
            ],
            rule,
            [
                "delete", "not_existing_rule",
            ]
        )

        self.assertIn("Error: {'result': 'not found'}\n", result.output)
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.plugin.firewall.rule.ApiClient.execute')
    def test_start_transaction_FAILED(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_savepoint_FAILED,
            ],
            rule,
            [
                "delete", "85282721-934c-42be-ba4d-a93cbfda26af",
            ],
            True
        )

        self.assertIn("Error: Savepoint creation failed: {'status': 'failed'}\n", result.output)
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.plugin.firewall.rule.ApiClient.execute')
    def test_commit_transaction_apply_FAILED(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_savepoint_OK,
                self._api_data_fixtures_delete_OK,
                self._api_data_fixtures_apply_FAILED

            ],
            rule,
            [
                "delete", "85282721-934c-42be-ba4d-a93cbfda26af",
            ],
            True
        )

        self.assertIn("Error: firewall rule apply failed: {'status': 'FAILED\\n\\n'}\n", result.output)
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.plugin.firewall.rule.ApiClient.execute')
    def test_commit_transaction_cancel_rollback_FAILED(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_savepoint_OK,
                self._api_data_fixtures_delete_OK,
                self._api_data_fixtures_apply_OK,
                self._api_data_fixtures_cancel_rollback_FAILED
            ],
            rule,
            [
                "delete", "85282721-934c-42be-ba4d-a93cbfda26af",
            ],
            True
        )

        self.assertIn(
            (
                "Error: firewall rule cancel rollback failed. "
                "Rollback configuration after 60 seconds: {'status': 'failed\\n\\n'}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)
