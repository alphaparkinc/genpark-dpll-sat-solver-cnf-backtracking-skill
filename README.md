# DPLL SAT Solver Skill

Complete implementation of the Davis-Putnam-Logemann-Loveland (DPLL) Boolean satisfiability solver.

```mermaid
flowchart TD
    CNF["CNF Clauses Input"] --> UP["Unit Propagation Loop"]
    UP --> Empty{"Empty Clause?"}
    Empty -- Yes --> Backtrack["Backtrack (UNSAT Branch)"]
    Empty -- No --> Pure["Pure Literal Elimination"]
    Pure --> AllSat{"All Clauses Satisfied?"}
    AllSat -- Yes --> SAT["SAT Assignment Returned"]
    AllSat -- No --> Branch["Branching on Variable"]
    Branch --> UP
```

## Features
- **100% Python Standard Library**: Pure recursive backtracking engine.
- **Unit Propagation & Pure Literal**: Efficient clause reduction.
- **MCP Server Ready**: Direct stdio JSON-RPC 2.0 tool interface.
