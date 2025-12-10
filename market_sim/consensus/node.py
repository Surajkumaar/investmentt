from .utils.crypto_utils import generate_keypair, sign_message
import json

class Node:
    def __init__(self, node_id, is_byzantine=False):
        self.id = node_id
        self.is_byzantine = is_byzantine
        self.received_messages = []
        self.output = None

        # Generate cryptographic keypair
        self.private_key, self.public_key = generate_keypair()

    def receive(self, messages):
        """
        messages: list of tuples (sender_id, message_dict, signature)
        """
        self.received_messages.extend(messages)

    def send(self, network, to_id, message):
        """
        Send a signed message to a specific node
        """
        msg_bytes = json.dumps(message, sort_keys=True).encode()
        signature = sign_message(self.private_key, msg_bytes)
        network.send(self.id, to_id, message, signature)

    def broadcast(self, network, message):
        """
        Broadcast message to all other nodes
        """
        for node_id in network.nodes:
            if node_id != self.id:
                # Byzantine node can optionally send wrong value
                if self.is_byzantine:
                    bad_message = {"value": 999, "path": message.get("path", [])}
                    self.send(network, node_id, bad_message)
                else:
                    self.send(network, node_id, message)
