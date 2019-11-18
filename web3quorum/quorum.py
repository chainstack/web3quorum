from eth_utils import to_tuple
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.module import Module


class Raft(Module):

    @property
    @to_tuple
    def cluster(self):
        return self.web3.manager.request_blocking("raft_cluster", [])

    @property
    def role(self) -> str:
        return self.web3.manager.request_blocking("raft_role", [])

    def add_peer(self, enode_url: str) -> int:
        return self.web3.manager.request_blocking("raft_addPeer", [enode_url])

    def remove_peer(self, raft_id: bool) -> None:
        return self.web3.manager.request_blocking("raft_removePeer", [raft_id])

    @property
    def leader(self) -> str:
        return self.web3.manager.request_blocking("raft_leader", [])


class Istanbul(Module):
    # TODO: Need to implement
    pass


class Web3Quorum(Web3):

    def __init__(self, *args, **kwargs):

        # add Raft and ibft apis
        kwargs['modules'] = kwargs.get('modules', {})
        kwargs['modules'].update({'raft': (Raft,), 'istanbul': (Istanbul, )})
        super().__init__(*args, **kwargs)

        # apply poa middleware
        self.middleware_onion.inject(geth_poa_middleware, layer=0)
