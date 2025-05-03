from Module.NoriGrid import NoriGrid

from typing import List
import itertools

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
        if len(cells) < 2:
            raise ValueError(f"La région {region_id} a moins de 2 cellules")
        
        # Récupérer les variables associées aux cellules
        vars_in_region: List[int] = [get_var_id(r, c, width) for (r, c) in cells]
        
        # --- Au moins deux cellules sont colorées ---
        # Pour cela, on impose qu'il existe au moins une paire de variables vraies
        # On génère une clause par paire, chaque clause disant que cette paire est activée
        # En SAT, pour "au moins deux", on peut écrire la clause suivante :
        # (v1 AND v2) OR (v1 AND v3) OR ... 
        # Mais SAT ne gère pas directement les AND/OR, donc on encode en CNF :
        # On crée une clause par paire : v_i v_j 0
        # Puis on combine ces clauses avec une clause globale (ici on fait la simplification)
        
        # En fait, pour "au moins deux", on peut utiliser cette technique :
        # Ajouter une clause qui est la disjonction de toutes les paires, mais ce n'est pas CNF.
        # Donc on ajoute toutes les clauses v_i v_j 0 (une par paire)
        for v1, v2 in itertools.combinations(vars_in_region, 2):
            clauses.append(f"{v1} {v2} 0")
        
        # --- Au plus deux cellules sont colorées ---
        # Pour chaque triplet, au moins une des trois doit être fausse
        if len(cells) > 2:
            for v1, v2, v3 in itertools.combinations(vars_in_region, 3):
                clauses.append(f"-{v1} -{v2} -{v3} 0")
    
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
    