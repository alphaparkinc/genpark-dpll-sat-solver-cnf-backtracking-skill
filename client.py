"""DPLL Boolean Satisfiability Solver.
100% Python Standard Library.
"""

class DPLLSolver:
    """Solves CNF formulas using the Davis-Putnam-Logemann-Loveland algorithm."""
    @staticmethod
    def solve(clauses):
        """clauses: list of lists of signed integers representing literals.
        Returns: assignment dict {var: bool} or None if UNSAT.
        """
        assignment = {}
        return DPLLSolver._dpll(clauses, assignment)

    @staticmethod
    def _dpll(clauses, assignment):
        changed = True
        while changed:
            changed = False
            if any(len(c) == 0 for c in clauses):
                return None
            if len(clauses) == 0:
                return assignment

            # Unit propagation
            unit = next((c[0] for c in clauses if len(c) == 1), None)
            if unit is not None:
                var = abs(unit)
                val = unit > 0
                assignment[var] = val
                clauses = DPLLSolver._simplify(clauses, unit)
                changed = True

        if any(len(c) == 0 for c in clauses):
            return None
        if len(clauses) == 0:
            return assignment

        # Pure literal elimination
        all_lits = [lit for c in clauses for lit in c]
        pure_lits = set()
        for lit in all_lits:
            if -lit not in all_lits:
                pure_lits.add(lit)
        for plit in pure_lits:
            var = abs(plit)
            val = plit > 0
            assignment[var] = val
            clauses = DPLLSolver._simplify(clauses, plit)

        if len(clauses) == 0:
            return assignment

        # Choose branching variable
        chosen_var = abs(clauses[0][0])
        
        # Try True branch
        res = DPLLSolver._dpll(DPLLSolver._simplify(clauses, chosen_var), {**assignment, chosen_var: True})
        if res is not None:
            return res
            
        # Try False branch
        return DPLLSolver._dpll(DPLLSolver._simplify(clauses, -chosen_var), {**assignment, chosen_var: False})

    @staticmethod
    def _simplify(clauses, assigned_lit):
        new_clauses = []
        for c in clauses:
            if assigned_lit in c:
                continue
            new_c = [lit for lit in c if lit != -assigned_lit]
            new_clauses.append(new_c)
        return new_clauses
