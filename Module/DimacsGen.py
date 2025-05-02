"""
Module pour transformer un terrain NoriNori en fichier DIMACS CNF.

Ce module fournit des fonctions pour convertir une grille NoriNori
en formule CNF au format DIMACS, en utilisant les règles définies dans
le module regles.py.
"""
from typing import List, Optional
from Module.NoriGrid import NoriGrid
from Module.regles import premiere_regle, deuxieme_regle, nombre_variables


def calculer_nombre_clauses(contenu_dimacs: str) -> int:
    """
    Calcule le nombre total de clauses dans le contenu DIMACS.
    
    Args:
        contenu_dimacs: Contenu DIMACS généré par les fonctions de règles
        
    Returns:
        Le nombre total de clauses (lignes non commentées)
    """
    return len([ligne for ligne in contenu_dimacs.strip().split('\n') 
                if ligne and not ligne.startswith('c')])

def generer_dimacs(grille: NoriGrid) -> str:
    """
    Génère le contenu complet du fichier DIMACS pour la grille donnée.
    
    Args:
        grille: Une grille où chaque cellule contient l'identifiant de sa région
        
    Returns:
        Le contenu complet du fichier DIMACS
    """
    # Générer les clauses pour les deux règles
    clauses_regle1: str = premiere_regle(grille)
    clauses_regle2: str = deuxieme_regle(grille)
    
    # Concaténer les clauses
    contenu_clauses: str = clauses_regle2 + clauses_regle1
    
    # Calculer le nombre de variables et de clauses
    num_vars: int = nombre_variables(grille)
    num_clauses: int = calculer_nombre_clauses(contenu_clauses)
    
    # Construire l'en-tête du fichier DIMACS
    en_tete: str = (
        f"c Fichier DIMACS CNF pour un puzzle NoriNori de taille {grille.width}x{grille.height}\n"
        f"p cnf {num_vars} {num_clauses}\n"
    )
    
    return en_tete + contenu_clauses

def ecrire_dimacs(grille: NoriGrid, chemin_fichier: str = 'clauses.cnf') -> None:
    """
    Écrit un fichier DIMACS pour la grille NoriNori donnée.
    Args:
        grille: Une grille où chaque cellule contient l'identifiant de sa région
        chemin_fichier: Chemin où écrire le fichier DIMACS (par défaut: 'clauses.cnf')
        
    Raises:
        IOError: Si l'écriture du fichier échoue
    """
    print(type(grille))
    try:
        with open(chemin_fichier, 'w', encoding='utf-8') as f:
            f.write(generer_dimacs(grille))
        print(f"Fichier DIMACS écrit avec succès: {chemin_fichier}")
    except IOError as e:
        print(f"Erreur lors de l'écriture du fichier DIMACS: {e}")
        raise

def valider_grille(Nori: NoriGrid) -> bool:
    """
    Valide une grille NoriNori.
    
    Args:
        grille: Une grille où chaque cellule contient l'identifiant de sa région
        
    Returns:
        True si la grille est valide, False sinon
        
    Raises:
        ValueError: Si la grille est invalide
    """
    if not Nori.grid:
        raise ValueError("La grille est vide")
    
    height: int = Nori.height
    width: int = Nori.width if height > 0 else 0
    
    if width == 0:
        raise ValueError("La grille a une largeur de 0")
    
    # Vérifier que toutes les lignes ont la même longueur
    for row in Nori.grid:
        if len(row) != width:
            raise ValueError("Les lignes de la grille n'ont pas toutes la même longueur")
    
    # Vérifier que chaque région a au moins 2 cellules
    for region_id, count in Nori.regions.items():
        if len(count) < 2:
            raise ValueError(f"La région {region_id} a seulement {len(count)} cellule(s)")
    
    return True

def convertir_grille(grille: List[List[int]], chemin_fichier: Optional[str] = None) -> str:
    """
    Convertit une grille NoriNori en fichier DIMACS et retourne le contenu.
    
    Args:
        grille: Une grille où chaque cellule contient l'identifiant de sa région
        chemin_fichier: Chemin où écrire le fichier DIMACS (optionnel)
        
    Returns:
        Le contenu du fichier DIMACS
        
    Raises:
        ValueError: Si la grille est invalide
    """
    # Valider la grille
    valider_grille(grille)
    
    # Générer le contenu DIMACS
    contenu_dimacs: str = generer_dimacs(grille)
    
    # Écrire le fichier si un chemin est spécifié
    if chemin_fichier:
        try:
            with open(chemin_fichier, 'w', encoding='utf-8') as f:
                f.write(contenu_dimacs)
            print(f"Fichier DIMACS écrit avec succès: {chemin_fichier}")
        except IOError as e:
            print(f"Erreur lors de l'écriture du fichier DIMACS: {e}")
            raise
    
    return contenu_dimacs

if __name__ == "__main__":
    grille_exemple: NoriGrid = NoriGrid(3, 3, 2)
    #ecrire_dimacs(grille_exemple, "DIMACS/exemple.cnf")    
    # Utilisation alternative avec le contenu retourné
    contenu: str = convertir_grille(grille_exemple)
    print("\nContenu du fichier DIMACS généré:")
    print(contenu)