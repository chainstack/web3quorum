# web3quorum ⛓

_A web3py extension that supports [Quorum](https://www.goquorum.com/) APIs: [RAFT](https://docs.goquorum.com/en/latest/Consensus/raft/) and [Istanbul](https://docs.goquorum.com/en/latest/Consensus/ibft/istanbul-rpc-api/)._

## Quick start

   - pip install web3quorum

   - Examples of usage

   ```python
   from web3 import HTTPProvider
   from web3quorum import Web3Quorum
   
   w3 = Web3Quorum(HTTPProvider('http://foo.bar'))
   
   # retrieve an info about cluster
   >>> w3.raft.cluster
   ({'ip': '31.247.117.573',
  'nodeId': 'db207d418bbbfcb0639f303259f62bf1da3c95aceb051f32cac8361a1c08276f4296f8e3f57833caac9c2aaa28a90158bf6eaf3f8ad602ac27a3e0ed6c8c765c',
  'p2pPort': 30303,
  'raftId': 2,
  'raftPort': 50400},
 {'ip': '54.84.81.417',
  'nodeId': 'c9391a893f9d3e44d820419259f2e441f209c0e4e1957ca3df35473f20f529c3c94fecb1e1c37e3bb0f15b74defd0db3c72a1b83d5f2d65d34dd7d255efdba0c',
  'p2pPort': 30303,
  'raftId': 1,
  'raftPort': 50400})
  
  # add new raft peer
  >>> w3.raft.add_peer('enode://db207d418bbbfcb0639f303259f62bf1da3c95aceb051f32cac8361a1c08276f4296f8e3f57833caac9c2aaa28a90158bf6eaf3f8ad602ac27a3e0ed6c8c765c@1.1.1.1:30303?discport=0&raftport=50400')
  2
  
  # delete raft peer
  >>> w3.raft.remove_peer(2)

  ```
  - Resolve enode or hostname to raft Id
  ```
  from web3quorum import enode_to_raft_id
  
  >>> enode_to_raft_id(api, 'enode://db207d418bbbfcb0639f303259f62bf1da3c95aceb051f32cac8361a1c08276f4296f8e3f57833caac9c2aaa28a90158bf6eaf3f8ad602ac27a3e0ed6c8c765c@1.1.1.1:30303')
  2
  
  - Use web3Quorum mocking object in your tests
  from web3quorum import Web3QuorumMock
  
  
  ```
