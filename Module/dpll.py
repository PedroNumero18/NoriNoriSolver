
"""
DPLL Algorithm Implementation
"""
from typing import Dict, List, Optional, Set
class DpllNode:
    def __init__(self, assignment: Dict[int, Optional[bool]], var: Optional[int] = None, 
                 value: Optional[bool] = None) -> None:
        self.assignment: Dict[int, Optional[bool]] = assignment.copy()
        self.var: Optional[int] = var
        self.value: Optional[bool] = value
        self.left: Optional[DpllNode] = None  # False branch
        self.right: Optional[DpllNode] = None  # True branch
        self.is_solution: bool = False

    def apply_assignment(clauses: List[List[int]], var: int, value: bool) -> Optional[List[List[int]]]:
        """Apply a variable assignment to the set of clauses."""
        lit: int = var if value else -var
        new_clauses: List[List[int]] = []
        
        for clause in clauses:
            if lit in clause:
                continue
            new_clause: List[int] = [l for l in clause if l != -lit]
            if not new_clause:
                return None
            new_clauses.append(new_clause)
        
        return new_clauses

    def dpll(clauses: List[List[int]], assignment: Dict[int, Optional[bool]], num_vars: int, node: Optional['DpllNode'] = None) -> bool:
        """DPLL algorithm implementation with binary tree representation."""
        if len(clauses) == 0:
            return True
        
        if any(len(clause) == 0 for clause in clauses):
            return False

        
        # Unit propagation
        while True:
            unit_found: bool = False
            for clause in clauses:
                if len(clause) == 1:
                    unit_found = True
                    lit: int = clause[0]
                    var: int = abs(lit)
                    val: bool = lit > 0
                    assignment[var] = val
                    
                    new_clauses: List[List[int]] = []
                    for c in clauses:
                        if lit in c:
                            continue
                        if -lit in c:
                            new_c: List[int] = [l for l in c if l != -lit]
                            if new_c:
                                new_clauses.append(new_c)
                            else:
                                return False
                        else:
                            new_clauses.append(c)
                    
                    clauses = new_clauses
                    break
            
            if not unit_found or not clauses:
                break
        
        # Pure literal elimination
        literals: Set[int] = set()
        for clause in clauses:
            literals.update(clause)
        
        pure_lits: Set[int] = set()
        for lit in literals:
            if -lit not in literals:
                pure_lits.add(lit)
        
        if pure_lits:
            for lit in pure_lits:
                var: int = abs(lit)
                if assignment[var] is None:
                    assignment[var] = bool(lit > 0)
                    clauses = [c for c in clauses if lit not in c]
        
        if len(clauses) == 0:
            return True
        
        # Choose variable and branch
        for var in range(1, num_vars + 1):
            if assignment[var] is None:
                # True branch
                true_assignment: Dict[int, Optional[bool]] = assignment.copy()
                true_assignment[var] = True
                new_clauses_true: Optional[List[List[int]]] = DpllNode.apply_assignment(clauses, var, True)
                
                true_node: DpllNode = DpllNode(true_assignment, var, True)
                if node:
                    node.right = true_node
                
                if new_clauses_true is not None and DpllNode.dpll(new_clauses_true, true_assignment, num_vars, true_node):
                    true_node.is_solution = True
                    for k, v in true_assignment.items():
                        assignment[k] = v
                    return True
                
                # False branch
                false_assignment: Dict[int, Optional[bool]] = assignment.copy()
                false_assignment[var] = False
                new_clauses_false: Optional[List[List[int]]] = self.apply_assignment(clauses, var, False)
                
                false_node: DpllNode = DpllNode(false_assignment, var, False)
                if node:
                    node.left = false_node
                    
                if new_clauses_false is not None and self.dpll(new_clauses_false, false_assignment, num_vars, false_node):
                    false_node.is_solution = True
                    for k, v in false_assignment.items():
                        assignment[k] = v
                    return True
                
                return False
        
        return True