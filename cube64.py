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

	def parcours_3D(self):
		position = [0,0,0]
		orientation = [1,0,0]
		self.occupation3D = []
		self.suite_orientation = [orientation]
		resultat = "terminé !"
		for i in range(0, self.nb_noeuds):
			nb_pas = self.instructions[i]
			#print(orientation)
			for p in range(0,nb_pas):
				nouvelle_position = np.array(position) + np.array(orientation)
				nouvelle_position = nouvelle_position.tolist()
				if nouvelle_position in self.occupation3D:
					resultat = "déjà passé par là"
					return i, resultat
				for c in self.occupation3D:
					if self.cube_condition(c, nouvelle_position) == 0:
						resultat = "on est sorti du cube"
						return i, resultat
				position = nouvelle_position
				self.occupation3D.append(position)
			directions_possible = self.filtrer_directions(orientation)
			gps = self.instructions_tourner[i]
			orientation = directions_possible[gps]
			self.suite_orientation.append(orientation)
		return i, resultat

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
		num_max, resultat = cube.parcours_3D()
		#print(resultat, self.instructions_tourner[:num_max])
		#print(self.suite_orientation)
		for i in range(0, 100000):
			self.instructions_tourner = self.incrementer_liste(self.instructions_tourner[:num_max]) + self.instructions_tourner[num_max:]
			num_max, resultat = cube.parcours_3D()
			#print(self.instructions_tourner[:num_max], resultat)
			if num_max > 48:
				break
		# for i in range(0,num_max):
		# 	print(self.suite_orientation[i], self.instructions[i])
		print(self.instructions_tourner)



if __name__ == "__main__":
	cube = cube64(cube_chaine)
	cube.instructions_tourner = [0, 0, 0, 0, 1, 1, 2, 1, 0, 1, 1, 3, 0, 0, 0, 2, 0, 2, 3, 1, 0, 0, 3, 2, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	#cube.affichage()
	cube.solver()