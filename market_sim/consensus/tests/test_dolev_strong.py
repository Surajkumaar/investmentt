from market_sim.consensus.network import SynchronousNetwork
from market_sim.consensus.node import Node
from market_sim.consensus.byzantine_broadcast import ByzantineBroadcast

def test_dolev_strong_broadcast():
    # Create nodes (1 Byzantine for testing)
    nodes = [Node(i, is_byzantine=(i==5)) for i in range(1, 6)]
    network = SynchronousNetwork(nodes)

    # Run Dolev-Strong Byzantine Broadcast
    protocol = ByzantineBroadcast(network, sender_id=1, f=1)
    result = protocol.run(value=1)

    print("Node outputs:", result)

    # Check that all honest nodes output 1
    honest_nodes = [n for n in nodes if not n.is_byzantine]
    assert all(result[n.id] == 1 for n in honest_nodes)
