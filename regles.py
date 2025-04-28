import math as m
from itertools import product
'''
On définit une liste de toutes les cases correspondantes à chaque zone de la grille
Par exemple, liste[0] sera une liste des cases contenues dans la zone 1
'''
def definition_zones(grille):
    taille = len(grille)
    if m.isqrt(taille)**2 != taille:                #On vérifie que la grille donnée soit bien de format carré
        print("Erreur de format de la grille !")    
        exit()

    dict_zones = {}

    for i in range(taille):
        if not(grille[i] in dict_zones):
            dict_zones[grille[i]] = []
        dict_zones[grille[i]].append(i+1)

    return list(dict_zones.values())


'''
On définit une liste de chaque case de la grille et de ses cases voisines
Par exemple, liste[0] sera [1,2,7] si la grille est de taille 6
'''
def definition_voisines(grille):
    taille = len(grille)
    cote = int(m.sqrt(taille))
    ensemble_cases_voisines = []

    for i in range(1,taille+1):
        clause = ''
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



def clauses_premmiere_regle(ensemble_fnd_fausses, ensemble_cases_voisines):
    clauses = ''

    for i in range(len(ensemble_fnd_fausses)):
        for j in range(len(ensemble_fnd_fausses[i])):
            for k in range(len(ensemble_fnd_fausses[i][j])):
                
                clauses = clauses + str(-ensemble_fnd_fausses[i][j][k] * ensemble_cases_voisines[i][k]) + ' '
            clauses += '\n'


    return clauses


    #Ci gît les vestiges de la fonction que nous voulions utiliser à la base, résultat de la formalisation en FNC que l'on peut retrouver dans le rapport
    #Nous n'avons malheuresement pas réussi à la faire fonctionner et nous sommes donc tournés vers la méthode de : table de vérité -> FND de -F -> FNC de F
    '''
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


def premiere_regle(grille):
    ensemble_cases_voisines = definition_voisines(grille)
    ensemble_fnd_fausses = []
    for voisines in ensemble_cases_voisines:
        table_verite = list(product((-1,1),repeat=len(voisines)))
        fnd_fausses = [i for i in table_verite if i.count(1)!=2 and i[0]==1]    #
        ensemble_fnd_fausses.append(fnd_fausses)        

    return clauses_premmiere_regle(ensemble_fnd_fausses, ensemble_cases_voisines)


def clauses_deuxieme_regle(ensemble_fnd_fausses, zones):
    clauses = ''

    for i in range(len(ensemble_fnd_fausses)):
        for j in range(len(ensemble_fnd_fausses[i])):
            for k in range(len(ensemble_fnd_fausses[i][j])):
                
                clauses = clauses + str(-ensemble_fnd_fausses[i][j][k] * zones[i][k]) + ' '
            clauses += '\n'

    return clauses


def deuxieme_regle(grille):
    zones = definition_zones(grille)
    ensemble_fnd_fausses = []
    for zone in zones:
        table_verite = list(product((-1,1),repeat=len(zone)))
        fnd_fausses = [i for i in table_verite if i.count(1)!=2]
        ensemble_fnd_fausses.append(fnd_fausses)        

    return clauses_deuxieme_regle(ensemble_fnd_fausses, zones)




    