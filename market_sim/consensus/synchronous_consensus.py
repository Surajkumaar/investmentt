from .network import SynchronousNetwork
from .node import Node

class SynchronousConsensus:
    """
    Simple synchronous consensus algorithm with signed messages.
    """

    def __init__(self, network):
        self.network = network

    def run(self, sender_input):
        # Assume node 1 is sender
        sender = self.network.nodes[1]
        sender.broadcast(self.network, {"value": sender_input, "path": [sender.id]})
        self.network.deliver_round()

        # Forward messages once for all nodes
        for node in self.network.nodes.values():
            for msg_tuple in node.received_messages:
                sender_id, msg, _ = msg_tuple  # unpack signed message
                if node.id not in msg.get("path", []):
                    new_msg = {"value": msg["value"], "path": msg["path"] + [node.id]}
                    node.broadcast(self.network, new_msg)

        self.network.deliver_round()

        # Decision: majority of received values
        outputs = {}
        for node in self.network.nodes.values():
            values = [msg[1]["value"] for msg in node.received_messages]
            if not values:
                outputs[node.id] = 0
            else:
                outputs[node.id] = max(set(values), key=values.count)

        return outputs
