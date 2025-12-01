##TP7 - Ex1 et 2
##voir photo pour dessin graphe d'ex et representation des matrices et listes d'adjacences

#Q1
"""Complexité en espace de la matrice d'adjacence est par n**2 avec n=|V|=la taille de la matrice.
    Mais liste[i] (listes d'adjacences) est de complexité d'espace de cst car liste.
    Ainsi, les listes d'adjacences sont plus optimale dans l'utilisation des ressources."""

#Q2
"""
Type représentation | Recherche de voisins | Ajout d'arête | Suppr d'arête | Test d'adja entre 2 sommets
--------------------|----------------------|---------------|---------------|---------------------------
Liste d'adjacence   |   O(k)               | O(1)          | O(k)          | O(k)
Matrice d'adja      |   O(n)               | O(1)          | O(1)          | O(1)
"""

#listes adja en tant que dico et test d'adja entre 2 sommetes via 2 dicos
#se poser les bonnes questions sur représentation


import numpy as np
mat_test=np.array([[0,1,1,0,0,0],
            [0,0,1,1,0,0],  
            [0,0,0,1,1,0],
            [0,0,0,0,1,1],
            [0,0,0,0,0,1],
            [0,0,0,0,0,0]])
mat_test2=np.array([[0,1,1,0],
            [1,0,1,1],
            [1,1,0,1],
            [0,1,1,0]]) 

#Verif si matrice est orienté# cad si sym
def oriente(M):
    if ...