"""Blockchain layer. Works in two modes:
 1) LOCAL (default): in-memory Ethereum test chain. Zero setup, real EVM + real smart contract.
 2) SEPOLIA/AMOY: set RPC_URL, PRIVATE_KEY (and CONTRACT_ADDRESS after first deploy) as environment variables.
"""
import hashlib, json, os
from web3 import Web3
from contract_data import ART


def record_hash(payload: dict) -> str:
    """SHA-256 fingerprint of a record. Any change in any field changes this hash."""
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class Chain:
    def __init__(self):
        rpc, pk = os.getenv("RPC_URL"), os.getenv("PRIVATE_KEY")
        self.live = bool(rpc and pk)
        if self.live:
            self.w3 = Web3(Web3.HTTPProvider(rpc))
            self.acct = self.w3.eth.account.from_key(pk)
            self.sender = self.acct.address
        else:
            from web3 import EthereumTesterProvider
            self.w3 = Web3(EthereumTesterProvider())
            self.sender = self.w3.eth.accounts[0]
        addr = os.getenv("CONTRACT_ADDRESS")
        if self.live and addr:
            self.contract = self.w3.eth.contract(address=Web3.to_checksum_address(addr), abi=ART["abi"])
        else:
            self.contract = self._deploy()

    def _send(self, fn):
        if not self.live:
            tx = fn.transact({"from": self.sender})
        else:
            built = fn.build_transaction({"from": self.sender, "nonce": self.w3.eth.get_transaction_count(self.sender)})
            signed = self.acct.sign_transaction(built)
            raw = getattr(signed, "raw_transaction", None) or signed.rawTransaction
            tx = self.w3.eth.send_raw_transaction(raw)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx)
        return receipt["transactionHash"].hex()

    def _deploy(self):
        factory = self.w3.eth.contract(abi=ART["abi"], bytecode=ART["bytecode"])
        if self.live:
            built = factory.constructor().build_transaction({"from": self.sender, "nonce": self.w3.eth.get_transaction_count(self.sender)})
            signed = self.acct.sign_transaction(built)
            raw = getattr(signed, "raw_transaction", None) or signed.rawTransaction
            tx = self.w3.eth.send_raw_transaction(raw)
        else:
            tx = factory.constructor().transact({"from": self.sender})
        receipt = self.w3.eth.wait_for_transaction_receipt(tx)
        print("CONTRACT DEPLOYED AT:", receipt["contractAddress"])
        return self.w3.eth.contract(address=receipt["contractAddress"], abi=ART["abi"])

    def add_event(self, tag: str, event_type: str, hash_hex: str) -> str:
        return self._send(self.contract.functions.addEvent(tag, event_type, bytes.fromhex(hash_hex)))

    def get_events(self, tag: str) -> list:
        n = self.contract.functions.eventCount(tag).call()
        out = []
        for i in range(n):
            t, h, by, ts = self.contract.functions.getEvent(tag, i).call()
            out.append({"event_type": t, "hash": h.hex(), "recorded_by": by, "timestamp": ts})
        return out
