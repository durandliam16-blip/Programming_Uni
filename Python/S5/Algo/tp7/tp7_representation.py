##TP7 - Ex1 et 2
##voir photo pour dessin graphe d'ex et representation des matrices et listes d'adjacences

import numpy as np
from typing import List, Dict, Union, Tuple, Sequence, Optional

# =============================================================================
# EXERCICE 1 : Les représentations d'un graphe
# =============================================================================

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

#Q3 - Verif si matrice est orienté cad si sym
def am_is_undirected(M) -> bool:
    sym = True
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] != M[j][i]:
                return False
    return sym

#Q4 - Définition des types : 

# AdjMatrix : Liste de listes d'entiers (0 = pas d'arête, >0 = poids)
AdjMatrix = List[List[int]]
# AdjLists : Dictionnaire où la clé est le sommet (str) et la valeur est :
# - soit une liste de voisins (si non pondéré)
# - soit une liste de tuples (voisin, poids) (si pondéré)
# Dict[str, List[Tuple[str, int]]] où le poids est 1 par défaut.
AdjLists = Dict[str, List[Tuple[str, int]]]

#Q1.1 : La valuation des arcs sur les focnctions fait que l'on doit utiliser des tuples (voisin, poids)

def al_is_undirected(adj_l: AdjLists) -> bool:
    """Q2.2 - Vérif si des listes d'adja représentent un graphe non orienté.
    + Pour tout arc u->v de poids w, il doit exister v->u de poids w."""
    for u, neighbors in adj_l.items():
        for v, weight in neighbors:
            # Vérifier si u est dans les voisins de v avec le même poids
            if v not in adj_l:
                return False
            # Recherche de u dans la liste de v
            found_reverse = False
            for v_neighbor, v_weight in adj_l[v]:
                if v_neighbor == u:
                    if v_weight != weight: # Asymétrie de poids
                        return False
                    found_reverse = True
                    break
            if not found_reverse:
                return False
    return True

def al_undirect(adj_l: AdjLists) -> None:
    """Q3.2 - 
    Transforme un graphe orienté en non orienté en ajoutant les arcs réciproques manquants.
    + Modifie le dictionnaire en place."""
    # On fait une copie des clés pour itérer sans modifier la structure pendant l'itération
    vertices = list(adj_l.keys())
    for u in vertices:
        for v, w in adj_l[u]:
            # S'assurer que v existe dans le graphe
            if v not in adj_l:
                adj_l[v] = []
            # Vérifier si l'arc v->u existe déjà
            exists = False
            for neighbor, weight in adj_l[v]:
                if neighbor == u:
                    exists = True
                    break
            # Si non, on l'ajoute
            if not exists:
                adj_l[v].append((u, w))


#Q4.2 - Conversion entre les représentations

def am_to_al(adj_m: AdjMatrix, vertices: Sequence[str] = ()) -> AdjLists:
    """Q4.2 - Convertit une matrice d'adjacence en listes d'adja"""
    n = len(adj_m)
    # Si pas de noms fournis, on nomme "1", "2", ... "n" (comme demandé)
    if not vertices:
        vertices = [str(i + 1) for i in range(n)]
    if len(vertices) != n:
        raise ValueError("Le nombre de sommets ne correspond pas à la taille de la matrice.")
    adj_l: AdjLists = {v: [] for v in vertices}
    for i in range(n):
        u = vertices[i]
        for j in range(n):
            weight = adj_m[i][j]
            if weight != 0: # Il y a une arête
                v = vertices[j]
                adj_l[u].append((v, weight))
    return adj_l

def al_to_am(adj_l: AdjLists) -> AdjMatrix:
    """Q4.2 - Convertit des listes d'adjacence en matrice d'adja"""    # On trie les sommets pour avoir un ordre déterministe (indices de matrice)
    vertices = sorted(list(adj_l.keys()))
    n = len(vertices)
    # Map nom -> index
    v_to_i = {name: i for i, name in enumerate(vertices)}
    # Init matrice n x n avec des 0
    adj_m = [[0 for _ in range(n)] for _ in range(n)]
    for u_name, neighbors in adj_l.items():
        if u_name not in v_to_i: continue # Cas de sécurité
        u_idx = v_to_i[u_name]
        for v_name, weight in neighbors:
            if v_name in v_to_i:
                v_idx = v_to_i[v_name]
                adj_m[u_idx][v_idx] = weight
    return adj_m



if __name__ == "__main__":

    #création de 2 matrices de test
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

    print("--- Test Exercice 1 ---")
    # Matrice exemple (graphe triangle 1-2-3)
    # Indices 0, 1, 2 correspondant à "A", "B", "C"
    m_test = [
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0]
    ]
    print(f"Is undirected (Matrix)? {am_is_undirected(m_test)}")
    
    # Conversion Matrix -> Lists
    l_test = am_to_al(m_test, ["A", "B", "C"])
    print(f"Adjacency Lists: {l_test}")
    
    # Check List Undirected
    print(f"Is undirected (List)? {al_is_undirected(l_test)}")