import matplotlib.pyplot as plt
from market_sim.consensus.network import SynchronousNetwork
from market_sim.consensus.node import Node
from market_sim.consensus.byzantine_broadcast import ByzantineBroadcast

def visualize_dolev_strong():
    # Create nodes (1 Byzantine for illustration)
    nodes = [Node(i, is_byzantine=(i==5)) for i in range(1, 6)]
    network = SynchronousNetwork(nodes)
    
    # Keep track of messages per round
    rounds_messages = []

    # Patch deliver_round to capture message counts
    original_deliver_round = network.deliver_round
    def patched_deliver_round():
        current_count = {node_id: len(network.message_queues[node_id]) for node_id in network.nodes}
        rounds_messages.append(current_count)
        original_deliver_round()
    network.deliver_round = patched_deliver_round

    # Run broadcast
    protocol = ByzantineBroadcast(network, sender_id=1, f=1)
    result = protocol.run(value=1)

    # Print final outputs
    print("Final node outputs:", result)

    # Plot messages per round
    for node_id in range(1, 6):
        node_counts = [round_dict[node_id] for round_dict in rounds_messages]
        plt.plot(range(1, len(rounds_messages)+1), node_counts, marker='o', label=f'Node {node_id}')

    plt.xlabel("Round")
    plt.ylabel("Messages in Queue")
    plt.title("Dolev–Strong Broadcast: Messages per Node per Round")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    visualize_dolev_strong()
