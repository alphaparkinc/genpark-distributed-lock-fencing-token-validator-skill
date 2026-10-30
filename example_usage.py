"""Example usage for Distributed Lock Fencing Token Validator."""
from client import DistributedLockFencingValidator

if __name__ == "__main__":
    grant = DistributedLockFencingValidator.grant_lock("res_order_999", "worker-node-1", last_fencing_token=100)
    print("Lock Granted:", grant)

    valid = DistributedLockFencingValidator.validate_fencing_token(101, 101, 1000, 5000)
    print("Validation Check:", valid)
