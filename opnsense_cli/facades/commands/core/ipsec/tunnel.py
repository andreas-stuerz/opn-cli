from opnsense_cli.api.core.ipsec import Tunnel
from opnsense_cli.facades.commands.base import CommandFacade


class IpsecTunnelFacade(CommandFacade):

    def __init__(self, tunnel_api: Tunnel):
        super().__init__()
        self._complete_model_data_cache = None
        self._tunnel_api = tunnel_api

    def list_phase1_tunnels(self):
        return self._tunnel_api.searchPhase1()['rows']

    def show_phase1_tunnels(self, ikeid):
        phase1_entries = self._tunnel_api.searchPhase1()['rows']
        entry = [item for item in phase1_entries if item['id'] == int(ikeid)]

        return entry

    def list_phase2_tunnels(self):
        return self._get_all_phase2_entries()

    def show_phase2_tunnels(self, uniqid):
        phase2_entries = self._get_all_phase2_entries()
        entry = [item for item in phase2_entries if item['uniqid'] == uniqid]

        return entry

    def _get_all_phase2_entries(self):
        results = []
        all_ikeids = self._get_all_ikeids()

        for ikeid in all_ikeids:
            entries = self._tunnel_api.searchPhase2(json={"ikeid": ikeid})['rows']
            for entry in entries:
                if entry:
                    results.append(entry)

        return results

    def _get_all_ikeids(self):
        phase1_entries = self._tunnel_api.searchPhase1()['rows']

        return [phase1_entry['id'] for phase1_entry in phase1_entries]
