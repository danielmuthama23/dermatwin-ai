"""Agent 8 — Blockchain Audit Agent.

Anchors a tamper-evident record of every scan/recommendation on Hedera
Consensus Service, and lets the dashboard verify that a stored twin
state hasn't been altered since it was produced.
"""

from hedera_client import get_audit_client, _hash_payload


def audit_scan(user_id: str, twin_state: dict) -> dict:
    client = get_audit_client()
    return client.log_event(user_id, "scan_completed", twin_state)


def audit_recommendation(user_id: str, kind: str, payload: dict) -> dict:
    client = get_audit_client()
    return client.log_event(user_id, f"recommendation:{kind}", payload)


def get_audit_trail(user_id: str | None = None) -> list[dict]:
    client = get_audit_client()
    return client.get_trail(user_id)


def verify_integrity(twin_state: dict, expected_hash: str) -> bool:
    """Recompute the hash of a twin state and compare to what was
    anchored — proves the stored data matches what was audited."""
    return _hash_payload(twin_state) == expected_hash
