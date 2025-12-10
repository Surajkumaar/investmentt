from market_sim.consensus.node import Node
from market_sim.consensus.network import SynchronousNetwork
from market_sim.consensus.synchronous_consensus import SynchronousConsensus

def test_basic_consensus():
    # 5 nodes, all honest
    nodes = [Node(i) for i in range(1, 6)]
    network = SynchronousNetwork(nodes)
    
    protocol = SynchronousConsensus(network)
    outputs = protocol.run(sender_input=1)

    print("Node outputs:", outputs)

    # Check that all nodes agree on the sender's value
    assert all(v == 1 for v in outputs.values())
