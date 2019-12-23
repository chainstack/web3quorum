from unittest.mock import Mock

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

    def add_learner(self, enode_url: str) -> int:
        return self.web3.manager.request_blocking("raft_addLearner", [enode_url])

    def promote_to_peer(self, raft_id: bool) -> bool:
        return self.web3.manager.request_blocking("raft_promoteToPeer", [raft_id])

    def add_peer(self, enode_url: str) -> int:
        return self.web3.manager.request_blocking("raft_addPeer", [enode_url])

    def remove_peer(self, raft_id: bool) -> None:
        return self.web3.manager.request_blocking("raft_removePeer", [raft_id])

    @property
    def leader(self) -> str:
        return self.web3.manager.request_blocking("raft_leader", [])


class Istanbul(Module):

    @to_tuple
    def get_validators(self) -> tuple:
        return self.web3.manager.request_blocking("istanbul_getValidators", [])

    @to_tuple
    def get_validators_at_hash(self, hash: str) -> tuple:
        return self.web3.manager.request_blocking("istanbul_getValidators", [hash])

    def discard(self, addr: str):
        return self.web3.manager.request_blocking("istanbul_discard", [addr])

    def propose(self, addr: str, auth: bool):
        return self.web3.manager.request_blocking("istanbul_propose", [addr, auth])

    @property
    def candidates(self):
        return self.web3.manager.request_blocking("istanbul_candidates", [])

    def get_snapshot(self):
        return self.web3.manager.request_blocking("istanbul_getSnapshot", [])

    def get_snapshot_at_hash(self, hash: str):
        return self.web3.manager.request_blocking("istanbul_getSnapshotAtHash", [hash])


class Web3Quorum(Web3):

    def __init__(self, *args, **kwargs):
        # add Raft and ibft apis
        kwargs['modules'] = kwargs.get('modules', {})
        kwargs['modules'].update({'raft': (Raft,), 'istanbul': (Istanbul,)})
        super().__init__(*args, **kwargs)

        # apply poa middleware
        self.middleware_onion.inject(geth_poa_middleware, layer=0)


attrs = {'raft.cluster': [{'ip': '1.2.3.4',
                           'nodeId': 'foo',
                           'p2pPort': 30303,
                           'raftId': 2,
                           'raftPort': 50400},
                          {'ip': '9.9.9.9',
                           'nodeId': 'bar',
                           'p2pPort': 30303,
                           'raftId': 1,
                           'raftPort': 50400},
                          ],
         'raft.add_learner.return_value': 1,
         'raft.promote_to_peer.return_value': True,
         'raft.add_peer.return_value': 1,
         'raft.remove_peer.return_value': None,
         'raft.role': 'verifier',
         'raft.leader': 'foo',
         'istanbul.get_validators.return_value': ('0x7100a64b994d363c793a489df0963006598c0760',),
         'istanbul.discard.return_value': None,
         'istanbul.propose.return_value': None,
         'istanbul.candidates': {'0x7100a64b994d363c793a489df0963006598c0760': False},
         'istanbul.get_snapshot.return_value': {
             'epoch': 30000,
             'hash': "0x9052a3b052045fb27e7d33d961314d7136bde52999312500d47911e143c5fcad",
             'number': 172093,
             'policy': 0,
             'tally': {},
             'validators': [],
             'votes': []
         }}

attrs.update({'istanbul.get_snapshot_at_hash.return_value': attrs['istanbul.get_snapshot.return_value']})
attrs.update({'istanbul.get_validators_at_hash.return_value': attrs['istanbul.get_validators.return_value']})

web3mock = Mock(**attrs)

Web3QuorumMock = Mock()
Web3QuorumMock.return_value = web3mock
