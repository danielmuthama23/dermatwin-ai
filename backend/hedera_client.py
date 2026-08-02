"""
Hedera (Hiero) audit client.

Every scan/recommendation the platform produces gets hashed and the hash
is submitted as a message to a Hedera Consensus Service (HCS) topic.
HCS timestamps and orders messages on a public, tamper-evident ledger,
so a retailer or regulator can later verify that a given recommendation
was produced at a given time and hasn't been altered after the fact —
this is the "security & auditing" role Hedera plays here, not payments
or token transfers.

Credentials load ONLY from environment variables (see .env.example).
If HEDERA_ACCOUNT_ID / HEDERA_PRIVATE_KEY aren't set, the client runs in
mock mode: it still computes and stores the audit hash locally (with a
clear `anchored_on_chain: False` flag) so the rest of the app and the
audit dashboard stay fully demoable offline.
"""

import hashlib
import json
import os
import time
from datetime import datetime, timezone
from typing import Any, Optional

from dotenv import load_dotenv

load_dotenv()

_LOCAL_AUDIT_LOG: list[dict] = []


def _hash_payload(payload: dict) -> str:
    canonical = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class HederaAuditClient:
    def __init__(self) -> None:
        self.account_id = os.getenv("HEDERA_ACCOUNT_ID")
        self.private_key = os.getenv("HEDERA_PRIVATE_KEY")
        self.topic_id = os.getenv("HEDERA_TOPIC_ID")
        self.network = os.getenv("HEDERA_NETWORK", "testnet")
        self._client = None

        if self.account_id and self.private_key:
            self._init_client()

    def _init_client(self) -> None:
        from hiero_sdk_python import Client, AccountId, PrivateKey

        self._client = Client.for_name(self.network) if hasattr(Client, "for_name") else Client()
        self._client.set_operator(
            AccountId.from_string(self.account_id),
            PrivateKey.from_string(self.private_key),
        )

    def is_live(self) -> bool:
        return self._client is not None and bool(self.topic_id)

    def ensure_topic(self) -> str:
        """Create an HCS topic once (e.g. during setup) and store its ID
        in HEDERA_TOPIC_ID. Exposed for a one-time setup script — not
        called automatically on every request."""
        from hiero_sdk_python import TopicCreateTransaction

        if not self._client:
            raise RuntimeError("Hedera client not configured.")
        receipt = (
            TopicCreateTransaction()
            .set_topic_memo("DermaTwin AI — recommendation audit trail")
            .execute(self._client)
        )
        topic_id = str(receipt.topic_id)
        self.topic_id = topic_id
        return topic_id

    def log_event(self, user_id: str, event_type: str, payload: dict) -> dict:
        """Hash + record an event. Submits to Hedera HCS if configured,
        otherwise stores locally in mock mode."""
        record = {
            "user_id": user_id,
            "event_type": event_type,
            "hash": _hash_payload(payload),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self.is_live():
            from hiero_sdk_python import TopicMessageSubmitTransaction, TopicId

            message = json.dumps({"user_id": user_id, "event_type": event_type, "hash": record["hash"]})
            receipt = (
                TopicMessageSubmitTransaction(
                    topic_id=TopicId.from_string(self.topic_id),
                    message=message,
                )
                .execute(self._client)
            )
            record["anchored_on_chain"] = True
            record["hedera_transaction_id"] = str(getattr(receipt, "transaction_id", ""))
            record["hedera_topic_id"] = self.topic_id
        else:
            record["anchored_on_chain"] = False
            record["hedera_transaction_id"] = None
            record["hedera_topic_id"] = None

        _LOCAL_AUDIT_LOG.append(record)
        return record

    def get_trail(self, user_id: Optional[str] = None) -> list[dict]:
        if user_id:
            return [r for r in _LOCAL_AUDIT_LOG if r["user_id"] == user_id]
        return list(_LOCAL_AUDIT_LOG)


_client_singleton: Optional[HederaAuditClient] = None


def get_audit_client() -> HederaAuditClient:
    global _client_singleton
    if _client_singleton is None:
        _client_singleton = HederaAuditClient()
    return _client_singleton
