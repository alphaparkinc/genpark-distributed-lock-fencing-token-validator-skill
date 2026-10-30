"""Distributed Lock Fencing Token Validator.
100% Python Standard Library.
"""

import time

class DistributedLockFencingValidator:
    """Enforces distributed mutual exclusion with monotonic fencing tokens to prevent split-brain writes."""

    @staticmethod
    def grant_lock(resource_key: str, client_id: str, last_fencing_token: int = 0,
                   lease_duration_ms: int = 5000) -> dict:
        now_ms = int(time.time() * 1000)
        new_token = last_fencing_token + 1
        lease_expiry = now_ms + lease_duration_ms

        return {
            "status": "GRANTED",
            "resource_key": resource_key,
            "client_id": client_id,
            "fencing_token": new_token,
            "granted_at_ms": now_ms,
            "lease_expiry_ms": lease_expiry,
            "lease_duration_ms": lease_duration_ms
        }

    @staticmethod
    def validate_fencing_token(incoming_token: int, current_active_token: int,
                               current_time_ms: int, lease_expiry_ms: int) -> dict:
        if incoming_token < current_active_token:
            return {
                "is_valid": False,
                "status": "STALE_TOKEN_REJECTED",
                "reason": f"Incoming token {incoming_token} is strictly older than active token {current_active_token}; split-brain write prevented"
            }

        if current_time_ms > lease_expiry_ms:
            return {
                "is_valid": False,
                "status": "LEASE_EXPIRED",
                "reason": f"Lock lease expired at {lease_expiry_ms} (current time {current_time_ms})"
            }

        return {
            "is_valid": True,
            "status": "VALID_COMMITTED",
            "fencing_token": incoming_token,
            "remaining_lease_ms": max(0, lease_expiry_ms - current_time_ms)
        }
