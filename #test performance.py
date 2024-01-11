import numpy as np

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

# Exemple d'utilisation
matrice_3d = [[[0, 1, 0, 0], [0, 0, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0]],
              [[0, 0, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]],
              [[0, 1, 0, 0], [1, 0, 0, 1], [0, 1, 1, 0], [0, 0, 1, 0]],
              [[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 0]]]

nombre_poches = compter_poches(matrice_3d)
print(nombre_poches)

