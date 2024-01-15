# usr/bin/env python3
# -*- coding: utf-8 -*-

"""
description du module :
cube_solver, l'objectif est de tester le maximum de combinaison pertinente
la méthode est d'identifier noeud qui pose problème pour ne pas tester toutes
les combinaisons de noeuds après
"""

from cube64_2 import *
import random
import math
import sqlite3
import json

def univers_init(dim=7):
	matrice_3d = np.zeros((dim, dim, dim), dtype=int)
	return matrice_3d

def volume(univers):
    indices = np.argwhere(univers == 1)
    if len(indices) == 0:
        return [0] 
    min_coords = np.min(indices, axis=0)
    max_coords = np.max(indices, axis=0)
    dimensions = max_coords - min_coords + 1
    return dimensions

def test_combinaison(cube, combinaison):
	cube.set_noeuds(combinaison)
	univers = univers_init()
	decalage = [3,3,3]
	orientation = [1,0,0]
	result = "reussi"

	for num, coord in enumerate(cube.get_coordonnees()):
		position = list(np.array(decalage) + np.array(coord))
		if not (all(0 <= c < 7 for c in position)):
			result = "sortie de l'univers"
			break
		if univers[tuple(position)] >= 1:
			result = "superposition"
			break
		if not all(dimension <= 4 for dimension in volume(univers)):
			result = "volume dépassant le 4x4x4"
			break
		if num > 15:
			nb_poche = compter_poches_cube(univers)
			if nb_poche > 1:
				result = "trop de poches {}".format(nb_poche)
				break
		if num > 20:
			nb_dead_end = compter_voisins_zeros(univers)
			nb_edge = compter_voisins_zeros(univers, 2)
			if nb_dead_end > 1:
				result = "trop de deadend {}".format(nb_dead_end)
				break
		univers[tuple(position)] += 1
	return cube.get_noeud_for_cubatome(num), result

def compter_poches_cube(matrice):
	if all(dimension == 4 for dimension in volume(matrice)):
		matrice = trouver_sous_matrice(matrice)
		return compter_poches(matrice)
	return compter_poches(matrice)

def trouver_sous_matrice(matrice):
    indices = np.argwhere(matrice == 1)
    if len(indices) == 0:
        return None  # Aucun "1" dans la matrice
    min_coords = np.min(indices, axis=0)
    max_coords = np.max(indices, axis=0) 
    # Extraire la sous-matrice
    sous_matrice = matrice[min_coords[0]:max_coords[0]+1,
                           min_coords[1]:max_coords[1]+1,
                           min_coords[2]:max_coords[2]+1]
    return sous_matrice

def incrementer_liste(listetotal, index=-1):
	liste = listetotal[:index]
	i = len(liste) - 1
	while i >= 0:
		if liste[i] < 3:
			liste[i] += 1
			break
		else:
			liste[i] = 0
			i -= 1
	return liste + listetotal[index:]

def incrementer_inverse(listetotal, index=0):
	liste = listetotal[index:]
	i = 0
	while i < len(liste)-1:
		if liste[i] < 3:
			liste[i] += 1
			break
		else:
			liste[i] = 0
			i += 1
	return listetotal[:index] + liste

def fourgits_to_base10(fourgits):
    return sum(val * (4 ** i) for i, val in enumerate(reversed(fourgits)))

def puissance_de_10_proche(nombre):
    # Calculer la puissance de 10 la plus proche en utilisant le logarithme en base 10
    if nombre == 0:
    	return 0
    if nombre < 0:
    	nombre = -nombre
    puissance = round(math.log10(nombre))
    return 10 ** puissance

def dfs(matrice, x, y, z, visite):
    # Vérifier si la position est dans la matrice et si le point n'a pas été visité et est un zéro
    if (0 <= x < len(matrice) and 0 <= y < len(matrice[0]) and 0 <= z < len(matrice[0][0])
            and not visite[x][y][z] and matrice[x][y][z] == 0):
        visite[x][y][z] = True  # Marquer comme visité

        # Appeler récursivement dfs sur tous les voisins adjacents
        dfs(matrice, x + 1, y, z, visite)
        dfs(matrice, x - 1, y, z, visite)
        dfs(matrice, x, y + 1, z, visite)
        dfs(matrice, x, y - 1, z, visite)
        dfs(matrice, x, y, z + 1, visite)
        dfs(matrice, x, y, z - 1, visite)

def compter_poches(matrice):
    visite = [[[False for _ in range(len(matrice[0][0]))] for _ in range(len(matrice[0]))] for _ in range(len(matrice))]
    nombre_poches = 0

    for x in range(len(matrice)):
        for y in range(len(matrice[0])):
            for z in range(len(matrice[0][0])):
                if matrice[x][y][z] == 0 and not visite[x][y][z]:
                    dfs(matrice, x, y, z, visite)
                    nombre_poches += 1  # Une nouvelle poche trouvée

    return nombre_poches

def inserer_donnees_batch(donnees):
    donnees_a_inserer = [(d['combinaison_num'], json.dumps(d['combinaison']), d['noeud'], d['resultat']) for d in donnees]
    cursor.executemany('INSERT INTO vitesse_convergence (combinaison_num, combinaison, noeud, resultat) VALUES (?, ?, ?, ?)', donnees_a_inserer)

def compter_voisins_zeros(matrice, nb_voisin=0):
    compteur = 0
    n = len(matrice)
    # Parcourir chaque élément de la matrice
    for x in range(n):
        for y in range(n):
            for z in range(n):
                if matrice[x][y][z] == 0:
                    # Compter les voisins qui sont également des zéros
                    voisins_zeros = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            for dz in [-1, 0, 1]:
                                # Ignorer les diagonales et l'élément lui-même
                                if abs(dx) + abs(dy) + abs(dz) != 1:
                                    continue
                                if 0 <= x + dx < n and 0 <= y + dy < n and 0 <= z + dz < n:
                                    if matrice[x + dx][y + dy][z + dz] == 0:
                                        voisins_zeros += 1

                    # Vérifier si l'élément a exactement un voisin zéro
                    if voisins_zeros == nb_voisin:
                        compteur += 1
    return compteur


# Connexion et création de la table
conn = sqlite3.connect('ma_base_de_donnees.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vitesse_convergence (
        id INTEGER PRIMARY KEY,
        combinaison_num TEXT,
        combinaison TEXT,
        noeud INTEGER,
        resultat TEXT
    )
''')


cube_chaine = [3,1,2,1,1,3,1,2,1,2,1,2,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,2,3,1,1,1,3,1,2,1,1,1,1,1,1,1,1,1,3,1]
cube = cube64(cube_chaine)
#first_digit = [0,1]
#combinaison = [2,2]
combinaison = [0 for i in range(0, cube.get_len_adn())]
noeud_moyen = 0
noeud_max = 0
noeud_moyen_section = 0
noeud_max_section = 0
n = 10000 #nombre de selection de combinaison aléatoire après les first_digits définis
m = 100 #nombre de recherche en incrémentant à partir d'une combinaison

print("longueur totale de la combinaison :", cube.get_len_adn())
#print("longueur des first_digit :", len(first_digit))
print("combinaison initiale : ", combinaison)
print("combinaison_num", fourgits_to_base10(combinaison))
#print("début boucle", first_digit)
# for i in range(0,4):
# 	for _ in range(0, n):
# 		combinaison = first_digit + [i]
# 		combinaison = combinaison + [random.randint(0, 3) for i in range(0, cube.get_len_adn()-len(combinaison))]
# 		for _ in range(0, m):
# 			noeud, res = test_combinaison(cube, combinaison)
# 			donnees = [{"combinaison_num": str(fourgits_to_base10(combinaison)), "combinaison": combinaison, "noeud": noeud, "resultat": res}]
# 			inserer_donnees_batch(donnees)
# 			noeud_moyen += noeud
# 			noeud_moyen_section += noeud
# 			if noeud > noeud_max:
# 				noeud_max = noeud
# 			if noeud > noeud_max_section:
# 				noeud_max_section = noeud
# 			if noeud < len(first_digit):
# 				break
# 			combinaison = incrementer_liste(combinaison, noeud+1)
# 	print(i, "noeud moyen :", round(noeud_moyen_section/(n*m), 2), "max atteint :", noeud_max_section)
# 	noeud_moyen_section = 0
# 	noeud_max_section = 0
for i in range(0, n):
	#combinaison = first_digit + [random.randint(0, 3) for i in range(0, cube.get_len_adn()-len(first_digit))]
	noeud, res = test_combinaison(cube, combinaison)
	donnees = [{"combinaison_num": str(fourgits_to_base10(combinaison)), "combinaison": combinaison, "noeud": noeud, "resultat": res}]
	inserer_donnees_batch(donnees)
	noeud_moyen += noeud
	if noeud > noeud_max:
		noeud_max = noeud	
	combinaison = incrementer_liste(combinaison, noeud+1)
	if (i+1)%100 ==0:
		print(i)

noeud_moyen = round(noeud_moyen/(n),2)
print("noeud moyen :", noeud_moyen)
print("noeud max :", noeud_max)
print(combinaison, noeud)
print("combinaison_num", fourgits_to_base10(combinaison))

cube.get_instruction()

conn.commit()
conn.close()