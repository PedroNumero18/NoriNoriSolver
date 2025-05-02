import math as m
from Module.NoriGrid import NoriGrid
from typing import List

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

def premiere_regle(Nori: NoriGrid)->str:
    height: int = Nori.height
    width: int = Nori.width if height > 0 else 0
    
    clauses: List[str] = []
    
    # Pour chaque région
    for region_id, cells in Nori.regions.items():
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

def deuxieme_regle(grille: NoriGrid)->str:
    """
    Génère les clauses CNF pour la deuxième règle : les cellules colorées ne peuvent pas se toucher par les côtés.
    Args:
        grille: Une grille où chaque cellule contient l'identifiant de sa région
    Returns:
        Une chaîne de caractères contenant les clauses CNF pour cette règle
    """
    height: int = grille.height
    width: int = grille.width if height > 0 else 0
    
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

def nombre_variables(Nori: NoriGrid) -> int:
    """
    Calcule le nombre total de variables nécessaires.
    
    Args:
        grille: Une grille où chaque cellule contient l'identifiant de sa région
        
    Returns:
        Le nombre total de variables (une par cellule)
    """
    height: int = Nori.height
    width: int = Nori.width if height > 0 else 0
    return height * width


if __name__ == "__main__":
    nr = NoriGrid(5, 5, 6)
    
    print("première règle: \n",premiere_regle(nr))
    print("deuxième règle: \n",deuxieme_regle(nr.grid))
    """
    try:
        with open('test.txt', 'w', encoding='utf-8') as f:
            f.write(deuxieme_regle(grille))
            f.write(premiere_regle(grille))
    except IOError as e:
        print(f"Erreur : {e}")
    """
    