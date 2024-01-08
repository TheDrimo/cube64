import numpy as np

def fixation(univers, position, orientation):
    # Calculer la position de départ pour la fixation
    position_debut = [p - 4 * o for p, o in zip(position, orientation)]

    # Vérifier et fixer les valeurs dans l'univers
    # Vérifier si la position de départ est dans les limites de l'univers
    if all(0 <= coord < 9 for coord in position_debut):
        # Fixer la valeur à 2 dans la couche correspondante
        if orientation[0] == 1:  # Axe des x
            univers[position_debut[0], :, :] = 2
        elif orientation[1] == 1:  # Axe des y
            univers[:, position_debut[1], :] = 2
        elif orientation[2] == 1:  # Axe des z
            univers[:, :, position_debut[2]] = 2

# Exemple d'utilisation
univers = np.zeros((9, 9, 9))
position = [5, 4, 4]
orientation = [1, 0, 0]
univers[tuple(position)] = 1

fixation(univers, position, orientation)
print(univers)  # Afficher la couche x = 1 de l'univers
