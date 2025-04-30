from regles import premiere_regle, deuxieme_regle

def ecrire_fichier(grille):
    grille = '112222134445133455163667166667666888'

    try:
        with open('clauses.cnf', 'w', encoding='utf-8') as f:
            f.write(deuxieme_regle(grille))
            f.write(premiere_regle(grille))
    except IOError as e:
        print(f"Erreur : {e}")
