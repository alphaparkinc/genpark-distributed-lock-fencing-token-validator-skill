"""MCP server for Distributed Lock Fencing Token Validator."""
import sys
import json
from client import DistributedLockFencingValidator

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "grant_lock",
                    "description": "Issue monotonic fencing token and lease duration for distributed resource",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "resource_key": {"type": "string"},
                            "client_id": {"type": "string"},
                            "last_fencing_token": {"type": "integer", "default": 0},
                            "lease_duration_ms": {"type": "integer", "default": 5000}
                        },
                        "required": ["resource_key", "client_id"]
                    }
                },
                {
                    "name": "validate_fencing_token",
                    "description": "Validate incoming fencing token against active token and lease expiration",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "incoming_token": {"type": "integer"},
                            "current_active_token": {"type": "integer"},
                            "current_time_ms": {"type": "integer"},
                            "lease_expiry_ms": {"type": "integer"}
                        },
                        "required": ["incoming_token", "current_active_token", "current_time_ms", "lease_expiry_ms"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "grant_lock":
            out = DistributedLockFencingValidator.grant_lock(
                args.get("resource_key", ""),
                args.get("client_id", ""),
                int(args.get("last_fencing_token", 0)),
                int(args.get("lease_duration_ms", 5000))
            )
            return {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]}
        elif name == "validate_fencing_token":
            out = DistributedLockFencingValidator.validate_fencing_token(
                int(args.get("incoming_token", 0)),
                int(args.get("current_active_token", 0)),
                int(args.get("current_time_ms", 0)),
                int(args.get("lease_expiry_ms", 0))
            )
            return {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]}
    return {"error": "Unsupported method or tool"}

if __name__ == "__main__":
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            print(json.dumps({"id": req.get("id"), "result": res}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()
