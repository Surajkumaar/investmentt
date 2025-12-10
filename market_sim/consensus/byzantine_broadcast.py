import json
from .utils.crypto_utils import sign_message, verify_signature

class ByzantineBroadcast:
    """
    Dolev–Strong Byzantine Broadcast with cryptographic signatures (simulation).
    Works in a synchronous network with authenticated messages.
    """

    def __init__(self, network, sender_id, f):
        self.network = network
        self.sender_id = sender_id
        self.f = f  # number of Byzantine nodes tolerated

    def run(self, value):
        """
        Execute f+1 rounds of message forwarding with signature verification.
        Returns final decided value for all nodes.
        """

        # -------- ROUND 0: sender broadcasts its value ----------
        sender = self.network.nodes[self.sender_id]
        message = {"value": value, "path": [sender.id]}
        sender.broadcast(self.network, message)
        self.network.deliver_round()

        # -------- ROUNDS 1 ... f -------------------------------
        for _ in range(self.f):
            for node in self.network.nodes.values():
                for sender_id, msg, sig in node.received_messages:
                    v = msg["value"]
                    path = msg["path"]

                    # Avoid loops
                    if node.id in path:
                        continue

                    # Verify signatures along the path
                    valid = True
                    for idx, node_in_path in enumerate(path):
                        pub_key = self.network.nodes[node_in_path].public_key
                        path_slice = {"value": v, "path": path[: idx + 1]}
                        path_bytes = json.dumps(path_slice, sort_keys=True).encode()
                        if not verify_signature(pub_key, path_bytes, sig):
                            valid = False
                            break
                    if not valid:
                        continue

                    # Forward message
                    new_msg = {"value": v, "path": path + [node.id]}
                    node.broadcast(self.network, new_msg)

            self.network.deliver_round()

        # -------- DECISION RULE (simple majority) --------------
        outputs = {}
        for node in self.network.nodes.values():
            values = [msg[1]["value"] for msg in node.received_messages]
            outputs[node.id] = max(set(values), key=values.count) if values else 0

        return outputs
