from Module.SatSolver import *
from Module.fichier import ecrire_fichier

def main():
    grille = '112222134445133455163667166667666888'
    ecrire_fichier(grille)

    solver = SatSolver()

    # Lire le fichier CNF
    with open("DIMACS/clauses.cnf", "r") as f:
        for line in f:
            if line.startswith('p') or line.startswith('c'):
                continue
            clause = list(map(int, line.strip().split()))
            solver.add_clause(clause)

    sat, solution = solver.solve()
    
    if sat:
        print("Solution :", [i for i in range(len(solution)) if solution[i]]) 
    else:
        print("Insatisfiable")



if __name__ == "__main__":
    main()