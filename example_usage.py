"""Example demonstrating DPLL SAT solving."""
from client import DPLLSolver

def main():
    # Formula: (x1 or x2) and (not x1 or x2) and (not x2 or x3)
    clauses = [[1, 2], [-1, 2], [-2, 3]]
    print("CNF Clauses:", clauses)
    sol = DPLLSolver.solve(clauses)
    print("DPLL Satisfying Assignment:", sol)

if __name__ == "__main__":
    main()
