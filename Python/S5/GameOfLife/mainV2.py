import random
import copy
import time
import sys
import subprocess

subprocess.run('', shell=True)

type Grid = list[list[int]]
GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

def ChangeEtat(M: Grid):
    M_new = copy.deepcopy(M)
    
    for y in range_coords:
        for x in range_coords:
            cell_nb_voisin = nbVoisins(M, x, y)

            if cell_nb_voisin in [0, 6]:
                M_new[y][x] = 0
            elif cell_nb_voisin in [1, 4]:
                M_new[y][x] = 1
    return M_new

def Imprime(M: Grid, i: int):
    print(f"\nEtape {i}")
    
    for collumn in M[1:-1]:
        print("|", end="") 
        for cell in collumn[1:-1]:
            print(str(cell) + "|", end="")
        print()
    for x in range (grid_size*2):
        sys.stdout.write("\033[F")

def ImprimeDifférence(M_init: Grid, M_new: Grid):
    print(''.join(['-' for _ in range(grid_size * 2 + 1)])) #precalculate it to make only one .join call
    for y in range(grid_size):
        print("|", end="")
        for x in range(grid_size):
            init = M_init[y + border_offset][x + border_offset]
            new = M_new[y + border_offset][x + border_offset]

            if init == new:
                cell = "-"
            elif init < new:
                cell = GREEN + "1" + ENDC
            else:
                cell = RED + "0" + ENDC
            
            print(cell + "|", end="")
        print()

def ConfigInit():
    a=int(input("Quel taille de grille ? "))
    grid_size = a
    border_offset = 1
    real_grid_size = grid_size + 2 * border_offset
    range_coords = range(border_offset, grid_size + border_offset)

    M = [[0 for i in range(real_grid_size)] for _ in range(real_grid_size)]
    print("The grid is initiated !")

    for y in range(grid_size):
        for x in range(grid_size):
            M[y+border_offset][x+border_offset] = random.randint(0, 1)

    nb_loop = int(input("Nombre de boucle du jeux de la vie à effectuer ?"))

    Imprime(M, 0)
    for i in range(nb_loop):
        M_new = ChangeEtat(M)
        Imprime(M_new, i+1)
        time.sleep(1.5)
        M = M_new
    
    return 

def nbVoisins(M: Grid, x: int, y: int):
    assert x > 0 and x <= grid_size and y > 0 and y <= grid_size 
    #meurt si sup à 4 ou inf à 1 cad vit pour 1,2 et 4

    total_voisin = 0
    if (M[y][x-1] == 1):
        total_voisin += 1
    if (M[y][x+1]):
        total_voisin += 1
    if (M[y-1][x] == 1):
        total_voisin += 1
    if (M[y+1][x]):
        total_voisin += 1
    if (M[y+1][x-1]):
        total_voisin += 1
    if (M[y-1][x+1]):
        total_voisin += 1
    
    return total_voisin

if __name__ == "__main__":
    ConfigInit()