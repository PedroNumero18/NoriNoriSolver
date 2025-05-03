import math as m
import random as rd
from Module.SatSolver import SatSolver
from Module.DimacsGen import ecrire_dimacs, convertir_grille
from Module.NoriGrid import NoriGrid
def main():
    while True:
        s = int(input("what size do you want\n")) 
        nbReg = (s**2)/2
        reg = rd.randint(1, m.floor(nbReg))
        Nori = NoriGrid(s, s, reg)
        Nori.printGrid()

        #generation du fichier dimacs
        ecrire_dimacs(Nori, "DIMACS/clauses.cnf")
        ans = input("souhaiter vous voir tout les clauses pour ce terrain ?\n")
        with open("DIMACS/clauses.cnf") as f:
            if ans.lower() == "oui" or ans.lower()== "yes":
                print(f.read())
            print("voici la solution au problème :")
            s = SatSolver()
            print(s.solve_file("DIMACS/clauses.cnf"))
        ans = input("do you want another NoriNori grid ?")
        if ans.lower() == "non" or ans.lower()== "no":
            break
if __name__ == "__main__":
    main()