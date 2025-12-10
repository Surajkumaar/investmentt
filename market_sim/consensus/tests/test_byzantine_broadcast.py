from market_sim.consensus.node import Node
from market_sim.consensus.network import SynchronousNetwork
from market_sim.consensus.byzantine_broadcast import ByzantineBroadcast

def test_byzantine_broadcast():
    nodes = [Node(i) for i in range(1, 6)]    # 5 nodes
    network = SynchronousNetwork(nodes)

    protocol = ByzantineBroadcast(network, sender_id=1, f=1)
    result = protocol.run(value=1)

    # All honest nodes must output 1
    assert all(v == 1 for v in result.values())
