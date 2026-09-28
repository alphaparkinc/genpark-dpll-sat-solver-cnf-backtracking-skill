"""MCP stdio server for DPLL SAT Solver."""
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import DPLLSolver

def handle_rpc(request):
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "solve_sat_cnf",
                        "description": "Solve Boolean satisfiability problem in CNF format via DPLL",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "clauses": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {"type": "integer"}
                                    },
                                    "description": "List of clauses (disjunction of signed integer literals)"
                                }
                            },
                            "required": ["clauses"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "solve_sat_cnf":
            clauses = args.get("clauses", [])
            sol = DPLLSolver.solve(clauses)
            if sol is None:
                return {"jsonrpc": "2.0", "id": req_id, "result": {"satisfiable": False, "assignment": None}}
            return {"jsonrpc": "2.0", "id": req_id, "result": {"satisfiable": True, "assignment": {str(k): v for k, v in sol.items()}}}
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method {name} not found"}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": "Invalid request"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_rpc(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
