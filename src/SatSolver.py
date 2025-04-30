"""
SAT Solver and DIMACS Parser Module

This module combines functionality for parsing DIMACS CNF format files and
solving Boolean satisfiability problems using the DPLL algorithm from dpll.py.
"""
from typing import Dict, List, Tuple, Optional, Set, Union
from dpll import dpll, DpllNode

class SatSolver:
    """
    A class that handles both parsing DIMACS CNF files and solving SAT problems.
    """
    
    def __init__(self) -> None:
        """Initialize the SAT solver."""
        self.num_vars: int = 0
        self.clauses: List[List[int]] = []
    
    def parse_dimacs(self, file_path: str) -> Tuple[int, List[List[int]]]:
        """
        Parse a DIMACS CNF file and return the number of variables and clauses.
        
        Args:
            file_path: Path to the DIMACS CNF file
            
        Returns:
            A tuple containing (number of variables, list of clauses)
            where each clause is a list of integers representing literals
            
        Raises:
            FileNotFoundError: If the input file cannot be found
            ValueError: If the file format is invalid
        """
        num_vars: int = 0
        num_clauses: int = 0
        clauses: List[List[int]] = []
        
        with open(file_path, 'r') as f:
            lines: List[str] = f.readlines()
            
            # Print debug info
            print(f"Read {len(lines)} lines from {file_path}")
            
            for line in lines:
                # Remove leading/trailing whitespace
                line = line.strip()
                
                # Skip empty lines and comment lines
                if not line or line.startswith('c'):
                    continue
                    
                # Parse problem line
                if line.startswith('p cnf'):
                    parts: List[str] = line.split()
                    if len(parts) != 4:
                        raise ValueError(f"Invalid problem line format: {line}")
                    try:
                        num_vars = int(parts[2])
                        num_clauses = int(parts[3])
                        print(f"Problem specification: {num_vars} variables, {num_clauses} clauses")
                    except ValueError:
                        raise ValueError(f"Invalid variable or clause count: {line}")
                else:
                    # Parse clause line
                    clause: List[int] = []
                    for lit in line.split():
                        try:
                            lit_val: int = int(lit)
                            if lit_val == 0:  # End of clause marker
                                if clause:
                                    clauses.append(clause)
                                    clause = []
                            else:
                                clause.append(lit_val)
                        except ValueError:
                            raise ValueError(f"Invalid literal in clause: {lit}")
                    
                    # Handle case where line doesn't end with 0
                    if clause:
                        clauses.append(clause)
        
        # Verify the number of clauses matches what was specified
        if num_clauses > 0 and len(clauses) != num_clauses:
            # Warning (removed logging dependency)
            # print(f"Warning: Number of clauses ({len(clauses)}) doesn't match specification ({num_clauses})")
            pass
        
        if num_vars == 0:
            raise ValueError("Missing or invalid problem specification line")
        
        # Store the parsed data as instance variables
        self.num_vars = num_vars
        self.clauses = clauses
        
        return num_vars, clauses
    
    def solve(self) -> Optional[Dict[int, bool]]:
        """
        Solve the SAT problem using the DPLL algorithm from dpll.py.
        
        Returns:
            Dictionary mapping variable numbers to boolean values (True/False),
            or None if the problem is unsatisfiable
        """
        # Create a deep copy of clauses to avoid modifying the original
        clauses_copy: List[List[int]] = [clause.copy() for clause in self.clauses]
        
        # Initialize assignment with None values (undecided)
        assignment: Dict[int, Optional[bool]] = {var: None for var in range(1, self.num_vars + 1)}
        
        # Create root node for DPLL decision tree (optional)
        root_node: DpllNode = DpllNode(assignment)
        
        # Run the DPLL algorithm from dpll.py
        result: bool = dpll(clauses_copy, assignment, self.num_vars, root_node)
        
        if result:
            # Ensure all variables have assignments (some might not be constrained)
            final_assignment: Dict[int, bool] = {}
            for var in range(1, self.num_vars + 1):
                if assignment[var] is None:
                    final_assignment[var] = True  # Arbitrary assignment for unconstrained variables
                else:
                    final_assignment[var] = assignment[var]  # type: ignore
            return final_assignment
        return None
    
    def solve_file(self, file_path: str) -> Optional[Dict[int, bool]]:
        """
        Parse a DIMACS CNF file and solve the SAT problem in one step.
        
        Args:
            file_path: Path to the DIMACS CNF file
            
        Returns:
            Dictionary mapping variable numbers to boolean values (True/False),
            or None if the problem is unsatisfiable
        """
        self.parse_dimacs(file_path)
        return self.solve()