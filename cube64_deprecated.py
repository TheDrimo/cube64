# usr/bin/env python3
# -*- coding: utf-8 -*-


"""
description du module :

définition de l'objet cube
plutôt que de voir la chaine de petit cube comme tel, il faut le voir comme une liste d'instruction à suivre
avec pour condition de ne jamais repasser sur ses pas
chaque petit cube de la chaine sont appelé cubatome
le grand cube qui doit être composé à partir de la chaine de cubatome est appelé cube64 ou bigcube

auteur : Nicolas Durmi
"""

import numpy as np
import random
import timeit


cube_chaine = [3,1,2,1,1,3,1,2,1,2,1,2,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,2,3,1,1,1,3,1,2,1,1,1,1,1,1,1,1,1,3,1]

class cube64:

	def __init__(self, instructions):
		self.instructions = instructions
		self.occupation2D = self.parcours_2D()
		self.occupation3D = self.occupation2D
		self.directions = self.liste_directions()
		self.nb_noeuds = len(instructions)
		self.instructions_tourner = [0]*self.nb_noeuds
		self.suite_orientation = []
		self.cube3d = self.univers_init()
		self.position = [4,4,4]

	def univers_init(self):
		"""
		on situe le cube au milieu d'un espace 9x9x9
		les bords sont signifiés par des 2
		"""
		matrice_3d = np.zeros((9, 9, 9), dtype=int)
		matrice_3d[0, :, :] = 2
		matrice_3d[:, 0, :] = 2
		matrice_3d[:, :, 0] = 2
		matrice_3d[-1, :, :] = 2
		matrice_3d[:, -1, :] = 2
		matrice_3d[:, :, -1] = 2
		return matrice_3d

	def chemin3d(self):
		self.cube3d = self.univers_init()
		self.position = [4,4,4]
		orientation = [1,0,0]
		changement = 0
		deplacement = 0
		self.suite_orientation = [orientation]
		resultat = "terminé"
		for pas in range(0,64):
			self.cube3d[tuple(self.position)] += 1
			deplacement += 1
			if self.cube3d[tuple(self.position)] > 1:
				resultat = "sorti de cube ou superposition"
				break
			if self.instructions[changement] == deplacement:
				directions_possible = self.filtrer_directions(orientation)
				print(orientation, directions_possible)
				orientation = directions_possible[self.instructions_tourner[changement]]
				self.suite_orientation.append(orientation)
				deplacement = 0
				changement += 1
			self.position = np.array(self.position) + np.array(orientation)
		return changement, resultat
 
	def parcours_2D(self):
		"""donne la liste de toutes les positions qu'occupent les cubatomes de la chaine de cubatome"""
		position = [0,0]
		orientation = 0 #0 pour avancer dans l'axe des x et 1 pour avancer dans l'axe des y
		chemin_parcouru = []
		for i in self.instructions:
			for p in range(0,i):
				if orientation == 0:
					position[0] += 1
				else:
					position[1] += 1
				chemin_parcouru.append(position.copy())
			orientation = 1 - orientation
		return chemin_parcouru

	def cube_condition(self, coord1, coord2, borne = 4):
		"""si tous les cubatomes sont compris dans le bigcube alors ils sont tous à une distance des uns des autres inférieur à 4
		cette fonction renvoie True la distance entre deux coordonnées est inférieur au maximum voulu"""
		d = max([abs(a - b) for a, b in zip(coord1, coord2)])
		condition = 0
		if d < borne :
			condition = 1
		return condition

	def liste_directions(self):
	    """
	    fais la liste des directions dans l'espace (vers les z croissants, les z descendant, les x croissants ...)
	    """
	    directions = []
	    for x in [-1, 1]:
	        directions.append([x, 0, 0])
	    for y in [-1, 1]:
	        directions.append([0, y, 0])
	    for z in [-1, 1]:
	        directions.append([0, 0, z])
	    return directions

	def dimension_pave(matrice, axe):
	    """
	    Calcule la dimension du pavé le long d'un axe donné (x, y ou z) dans une matrice 3D.

	    :param matrice: La matrice 3D contenant les éléments.
	    :param axe: L'axe le long duquel calculer la dimension ('x', 'y' ou 'z').
	    :return: La dimension du pavé le long de l'axe spécifié.
	    """
	    # Dictionnaire pour mapper les axes 'x', 'y', 'z' aux indices 0, 1, 2
	    axe_to_index = {'x': 0, 'y': 1, 'z': 2}

	    # Trouver les indices où les valeurs sont égales à 1
	    indices = np.argwhere(matrice == 1)

	    # Calculer la dimension le long de l'axe spécifié
	    min_val, max_val = np.min(indices[:, axe_to_index[axe]]), np.max(indices[:, axe_to_index[axe]])
	    return max_val - min_val + 1

	def filtrer_directions(self, direction_filtre=[1,0,0]):
	    """
	    donne toutes les directions perpendiculaires à la direction donnée (axe_filtre)
	    """
	    return [d for d in self.directions if not any((df != 0 and d[i] != 0) for i, df in enumerate(direction_filtre))]

	def affichage(self, axe="z"):
		print(sum(self.instructions))
		print(self.occupation2D)
		xmax, ymax = self.occupation2D[-1]
		planxy = np.zeros((xmax+1, ymax+1))
		for i in self.occupation2D:
			x, y = i
			planxy[x, y] = 1
		planxy = planxy.T
		lignes_en_chaine = [''.join(['x' if cell == 1 else ' ' for cell in ligne]) for ligne in planxy]
		for ligne in lignes_en_chaine:
		    print(ligne)

	def incrementer_liste(self, liste):
	    i = len(liste) - 1
	    while i >= 0:
	        if liste[i] < 3:
	            liste[i] += 1
	            break
	        else:
	            liste[i] = 0
	            i -= 1
	    return liste

	def solver(self):
		num_max, resultat = cube.chemin3d()
		for i in range(0, 10):
			self.instructions_tourner = self.incrementer_liste(self.instructions_tourner[:num_max]) + self.instructions_tourner[num_max:]
			num_max, resultat = cube.chemin3d()
		#print(self.cube3d)
		print(self.instructions_tourner, resultat)


if __name__ == "__main__":
	cube = cube64(cube_chaine)
	cube.affichage()
	cube.instructions_tourner = [0, 0, 0, 0, 1, 1, 2, 1, 0, 2, 0, 3, 2, 2, 1, 3, 1, 3, 1, 1, 0, 2, 2, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	#cube.affichage()
	cube.solver()

	# n = 10
	# temps_v1 = timeit.timeit('cube.solver()', globals=globals(), number=n)
	# temps_v2 = timeit.timeit('cube.solver2()', globals=globals(), number=n)
	# print(temps_v1, temps_v2)