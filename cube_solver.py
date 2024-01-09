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

def univers_init(dim=7):
	matrice_3d = np.zeros((dim, dim, dim), dtype=int)
	return matrice_3d

def volume(univers):
    indices = np.argwhere(univers == 1)
    if len(indices) == 0:
        return True 
    min_coords = np.min(indices, axis=0)
    max_coords = np.max(indices, axis=0)
    dimensions = max_coords - min_coords + 1
    return all(dimension <= 4 for dimension in dimensions)

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
		elif univers[tuple(position)] >= 1:
			result = "superposition"
			break
		elif not volume(univers):
			result = "volume dépassant le 4x4x4"
			break
		univers[tuple(position)] += 1
	return cube.get_noeud_for_cubatome(num), result

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


cube_chaine = [3,1,2,1,1,3,1,2,1,2,1,2,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,2,3,1,1,1,3,1,2,1,1,1,1,1,1,1,1,1,3,1]
cube = cube64(cube_chaine)
combinaison = [random.randint(0, 3) for i in range(0, cube.get_len_adn())]
combinaison_default = [0 for i in range(0, cube.get_len_adn())]

for i in range(0, 100000):
	noeud, res = test_combinaison(cube, combinaison_default)
	if res != "reussi":
		combinaison_default = incrementer_liste(combinaison_default, noeud)
	else:
		print(combinaison_default)
print(combinaison_default)


