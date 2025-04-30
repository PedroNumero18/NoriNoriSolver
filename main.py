from src.SatSolver import *
from src.fichier import ecrire_fichier

grille = '112222134445133455163667166667666888'
ecrire_fichier(grille)

s = Solver()

# Lire le fichier CNF
with open("DIMACS/clauses.cnf", "r") as f:
    for line in f:
        if line.startswith('p') or line.startswith('c'):
            continue
        clause = list(map(int, line.strip().split()))
        s.add_clause(clause)

sat, solution = s.solve()
if sat:
    print("Solution :", [i for i in range(len(solution)) if solution[i]]) 
else:
    print("Insatisfiable")