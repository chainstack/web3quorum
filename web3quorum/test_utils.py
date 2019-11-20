import unittest

from web3quorum import Web3QuorumMock
from web3quorum import utils

web3mock = Web3QuorumMock()


class TestUtils(unittest.TestCase):

    def test_enode_url_to_raft_id(self):
        raft_id = utils.enode_to_raft_id(web3mock, 'enode://foo@hostname?bar')

        assert raft_id == 2

    def test_enode_to_raft_id(self):
        raft_id = utils.enode_to_raft_id(web3mock, 'foo')

        assert raft_id == 2

    def test_ip_to_raft_id(self):
        raft_id = utils.ip_to_raft_id(web3mock, '1.2.3.4')

        assert raft_id == 2

    def test_enode_to_raft_id_none(self):
        raft_id = utils.enode_to_raft_id(web3mock, 'non-existing')

        assert raft_id is None
