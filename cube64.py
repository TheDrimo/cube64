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


adn_cube = [3,1,2,1,1,3,1,2,1,2,1,2,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,2,3,1,1,1,3,1,2,1,1,1,1,1,1,1,1,1,3,1]

class cube64:


	def __init__(self, adn):
		self.adn = adn
		self.schema = self.schema2D(adn) #string pour visualiser la forme de la chainette disposé à plat et en escalier
		self.combinaison = [0]*len(adn)
		self.univers = self.univers_init()

	def schema2D(self, instructions):
	    # Calcul du chemin parcouru
	    position = [0, 0]
	    orientation = 0  # 0 pour l'axe des x, 1 pour l'axe des y
	    chemin_parcouru = []

	    for i in instructions:
	        for _ in range(i):
	            position[orientation] += 1
	            chemin_parcouru.append(position.copy())
	        orientation = 1 - orientation

	    # Création du plan 2D
	    xmax, ymax = np.max(chemin_parcouru, axis=0)
	    planxy = np.zeros((xmax+1, ymax+1))

	    for x, y in chemin_parcouru:
	        planxy[x, y] = 1

	    planxy = planxy.T
	    lignes_en_chaine = [''.join(['x' if cell == 1 else ' ' for cell in ligne]) for ligne in planxy]

	    # Construction de la chaîne de caractères pour l'affichage
	    affichage = '\n'.join(lignes_en_chaine)
	    return affichage

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

	def fixation(self, position, orientation):
		# Calculer la position de départ pour la fixation
		position_debut = np.array(position) - 4*np.array(orientation)
		#print("fixation", position_debut, orientation)
		# Vérifier et fixer les valeurs dans l'univers
		# Vérifier si la position de départ est dans les limites de l'univers
		if all(0 <= coord < 9 for coord in position_debut):
	    	# Fixer la valeur à 2 dans la couche correspondante
			if abs(orientation[0]) == 1:
				self.univers[position_debut[0],:,:]=2
			elif abs(orientation[1]) == 1:  # Axe des y
				self.univers[:, position_debut[1], :] = 2
			elif abs(orientation[2]) == 1:  # Axe des z
				self.univers[:, :, position_debut[2]] = 2

	def cubage(self):
	    # Trouver les indices où les valeurs sont égales à 1
	    indices = np.argwhere(self.univers == 1)

	    # Trouver les dimensions du cubage des "1"
	    if len(indices) == 0:
	        return False  # Aucun "1" dans la matrice

	    min_coords = np.min(indices, axis=0)
	    max_coords = np.max(indices, axis=0)
	    dimensions = max_coords - min_coords + 1

	    # Vérifier si les dimensions sont 4x4x4
	    return all(dimension != 4 for dimension in dimensions)

	def virage(self, pas,orientation, tournant):
		print(sum(self.adn[:tournant]), pas)
		if (sum(self.adn[:tournant]) == pas+1):
			tournant += 1
			directions = cube64.liste_directions()
			directions = cube64.filtrer_directions(directions, orientation)
			orientation = directions[self.combinaison[tournant]]
			print("je tourne vers ", orientation)
			return orientation, tournant
		return orientation, tournant

	def liste_directions():
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

	def filtrer_directions(directions, direction_filtre=[1,0,0]):
	    """
	    donne toutes les directions perpendiculaires à la direction donnée (axe_filtre)
	    """
	    return [d for d in directions if not any((df != 0 and d[i] != 0) for i, df in enumerate(direction_filtre))]

	def chemin(self):
		self.univers = self.univers_init()
		position = [4,4,4]
		orientation = [1,0,0]
		flottant = True
		valide = True
		tournant = 1
		for pas in range(0,64):
			self.univers[tuple(position)] += 1
			#vérifier les conditions de validité
			if self.univers[tuple(position)] > 1:
				valide = False
				print("sortie ou superposition")
				#print(self.univers)
				break
			if flottant:
				self.fixation(position, orientation)
				flottant = self.cubage()
			orientation, tournant = self.virage(pas, orientation, tournant)
			position = np.array(position) + np.array(orientation)
			#print(position)
			#print(self.univers)
		return tournant

def incrementer_liste(liste):
    i = len(liste) - 1
    while i >= 0:
        if liste[i] < 3:
            liste[i] += 1
            break
        else:
            liste[i] = 0
            i -= 1
    return liste

def solver():
	cube = cube64(adn_cube)
	print(cube.schema)
	#cube.combinaison = [0, 0, 0, 0, 1, 1, 2, 1, 0, 2, 0, 3, 2, 2, 1, 3, 1, 3, 1, 1, 0, 2, 2, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	for n in range(0, 100):
		max_virage = cube.chemin()
		print(cube.combinaison, max_virage)
		cube.combinaison = incrementer_liste(cube.combinaison[:max_virage]) + cube.combinaison[max_virage:]
		print(cube.combinaison)
	#print(cube.univers)

if __name__ == "__main__":
	solver()