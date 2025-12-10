from .utils.crypto_utils import sign_message, verify_signature
import json

class SynchronousNetwork:
    def __init__(self, nodes):
        self.nodes = {node.id: node for node in nodes}
        # Queue stores tuples: (sender_id, message, signature)
        self.message_queues = {node.id: [] for node in nodes}

    def send(self, sender_id, to_id, message, signature):
        """Send message with signature to a single node"""
        self.message_queues[to_id].append((sender_id, message, signature))

    def deliver_round(self):
        """Deliver all messages for this round to nodes"""
        current_messages = self.message_queues
        self.message_queues = {node_id: [] for node_id in self.nodes}

        for node_id, messages in current_messages.items():
            node = self.nodes[node_id]
            valid_messages = []
            for sender_id, message, signature in messages:
                # Verify signature of sender
                pub_key = self.nodes[sender_id].public_key
                msg_bytes = json.dumps(message, sort_keys=True).encode()
                if verify_signature(pub_key, msg_bytes, signature):
                    valid_messages.append((sender_id, message, signature))
            node.receive(valid_messages)
