import math as m
from NoriGrid import NoriNori 
from itertools import product
from typing import List, Dict, Tuple
'''
On définit une liste de toutes les cases correspondantes à chaque zone de la grille
Par exemple, liste[0] sera une liste des cases contenues dans la zone 1
'''
'''
def definition_zones(grille: list[list[tuple[int, int, bool]]]) -> list[list[int]]:
    taille = len(grille[0][0])
    dict_zones = {}
    
    for i in range(taille):
        if not(grille[i][1] in dict_zones):
            dict_zones[grille[i][1]] = []
        dict_zones[grille[i][1]].append(i+1)

    return list(dict_zones.values())

def definition_voisines(grille: str)-> list[list[int]]:
    taille = len(grille)
    cote = int(m.sqrt(taille))
    ensemble_cases_voisines = []

    for i in range(1,taille+1):
        cases_voisines = []
        cases_voisines.append(i)

        if i%cote != 1:
            cases_voisines.append(i-1)
        if i%cote != 0:
            cases_voisines.append(i+1)
        if i > cote:
           cases_voisines.append(i-cote)
        if i <= taille - cote:
            cases_voisines.append(i+cote)
        
        ensemble_cases_voisines.append(cases_voisines)

    return ensemble_cases_voisines

def clauses_premmiere_regle(ensemble_fnd_fausses: list[tuple[int]], ensemble_cases_voisines: list[list[int]])->str:
    clauses = ''

    for i in range(len(ensemble_fnd_fausses)):
        for j in range(len(ensemble_fnd_fausses[i])):
            for k in range(len(ensemble_fnd_fausses[i][j])):
                
                clauses = clauses + str(-ensemble_fnd_fausses[i][j][k] * ensemble_cases_voisines[i][k]) + ' '
            clauses += '\n'
    return clauses


    #Ci gît les vestiges de la fonction que nous voulions utiliser à la base, résultat de la formalisation en FNC que l'on peut retrouver dans le rapport
    #Nous n'avons malheuresement pas réussi à la faire fonctionner et nous sommes donc tournés vers la méthode de : table de vérité -> FND de -F -> FNC de F
    
    clauses = ''
    matrices = [
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,1,1],
            [-1,-1,1,-1,1],
            [-1,-1,1,1,-1],
            [-1,1,-1,-1,1],
            [-1,1,-1,1,-1],
            [-1,1,1,-1,-1],
            [-1,1,1,1,1]
    ]
    for k in ensemble_cases_voisines:
        for i in range(8):
            for j in range(5):
                if k[j] != 0:
                    clauses = clauses + str(k[j] * matrices[i][j]) + ' '
            clauses += '\n'

    return clauses
    
'''
def get_var_id(row: int, col: int, width: int) -> int:
    """
    Calcule l'identifiant de variable pour une cellule spécifique.
    
    Args:
        row: Numéro de ligne (0-indexé)
        col: Numéro de colonne (0-indexé)
        width: Largeur de la grille
        
    Returns:
        L'identifiant de variable pour cette cellule (1-indexé pour DIMACS)
    """
    return row * width + col + 1

def premiere_regle(grille: list[list])->str:
    height: int = len(grille)
    width: int = len(grille[0]) if height > 0 else 0
    
    # Grouper les cellules par région
    regions: Dict[int, List[Tuple[int, bool]]] = {}
    for r in range(height):
        for c in range(width):
            region_id: int = grille[r][c]
            if region_id not in regions:
                regions[region_id] = []
            regions[region_id].append((r, c))
    
    clauses: List[str] = []
    
    # Pour chaque région
    for region_id, cells in regions.items():
        # Au moins 2 cellules sont colorées (si une région a moins de 2 cellules, problème)
        if len(cells)<2 :
            raise ValueError(f"La région {region_id} a moins de 2 cellules")
            
        # Au moins 2 cellules sont colorées
        at_least_two: List[int] = []
        for r, c in cells:
            var_id: int = get_var_id(r, c, width)
            at_least_two.append(var_id)
        clauses.append(" ".join(map(str, at_least_two)) + " 0")
        
        # Pas plus de 2 cellules sont colorées
        # Pour chaque combinaison de 3 cellules, au moins une doit être non colorée
        if len(cells) > 2:
            for i in range(len(cells)):
                for j in range(i + 1, len(cells)):
                    for k in range(j + 1, len(cells)):
                        r1, c1 = cells[i]
                        r2, c2 = cells[j]
                        r3, c3 = cells[k]
                        var1: int = get_var_id(r1, c1, width)
                        var2: int = get_var_id(r2, c2, width)
                        var3: int = get_var_id(r3, c3, width)
                        
                        # Au moins une des trois variables doit être fausse
                        clauses.append(f"-{var1} -{var2} -{var3} 0")
    
    # Ajouter un commentaire expliquant ces clauses
    header: str = "c Règle 1: Chaque région doit contenir exactement 2 cellules colorées\n"
    return header + "\n".join(clauses) + "\n"

def deuxieme_regle(grille: list[list])->str:
    """
    Génère les clauses CNF pour la deuxième règle : les cellules colorées ne peuvent pas se toucher par les côtés.
    Args:
        grille: Une grille où chaque cellule contient l'identifiant de sa région
    Returns:
        Une chaîne de caractères contenant les clauses CNF pour cette règle
    """
    height: int = len(grille)
    width: int = len(grille[0]) if height > 0 else 0
    
    clauses: List[str] = []
    
    # Pour chaque paire de cellules adjacentes
    for r in range(height):
        for c in range(width):
            var_id: int = get_var_id(r, c, width)
            
            # Vérifier la cellule à droite
            if c + 1 < width:
                var_right: int = get_var_id(r, c + 1, width)
                # Pas deux cellules adjacentes colorées
                clauses.append(f"-{var_id} -{var_right} 0")
            
            # Vérifier la cellule en dessous
            if r + 1 < height:
                var_below: int = get_var_id(r + 1, c, width)
                # Pas deux cellules adjacentes colorées
                clauses.append(f"-{var_id} -{var_below} 0")
    
    # Ajouter un commentaire expliquant ces clauses
    header: str = "c Règle 2: Les cellules colorées ne peuvent pas se toucher par les côtés\n"
    return header + "\n".join(clauses) + "\n"

def nombre_variables(grille: List[List[int]]) -> int:
    """
    Calcule le nombre total de variables nécessaires.
    
    Args:
        grille: Une grille où chaque cellule contient l'identifiant de sa région
        
    Returns:
        Le nombre total de variables (une par cellule)
    """
    height: int = len(grille)
    width: int = len(grille[0]) if height > 0 else 0
    return height * width


if __name__ == "__main__":
    grille: List[List[int]] = [
        [1, 1],
        [2, 2]
    ]
    
    print("première règle: \n",premiere_regle(grille))
    print("deuxième règle: \n",deuxieme_regle(grille))
    """
    try:
        with open('test.txt', 'w', encoding='utf-8') as f:
            f.write(deuxieme_regle(grille))
            f.write(premiere_regle(grille))
    except IOError as e:
        print(f"Erreur : {e}")
    """
    