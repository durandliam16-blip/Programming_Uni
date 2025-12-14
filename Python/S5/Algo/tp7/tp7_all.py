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

#Verif si matrice est orienté cad si sym
def oriente(M):
    sym = True
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] != M[j][i]:
                return False
    return sym



import math
import random
from typing import List, Dict, Union, Tuple, Sequence, Optional

# =============================================================================
# EXERCICE 1 : Les représentations d'un graphe
# =============================================================================

# Définition des types (Page 3, Q3 & Q4)
# AdjMatrix : Liste de listes d'entiers (0 = pas d'arête, >0 = poids)
AdjMatrix = List[List[int]]

# AdjLists : Dictionnaire où la clé est le sommet (str) et la valeur est :
# - soit une liste de voisins (si non pondéré)
# - soit une liste de tuples (voisin, poids) (si pondéré)
# Pour simplifier et unifier la gestion pondérée/non pondérée dans les fonctions,
# nous utiliserons une structure flexible ici, mais le standard sera :
# Dict[str, List[Tuple[str, int]]] où le poids est 1 par défaut.
AdjLists = Dict[str, List[Tuple[str, int]]]

def am_is_undirected(adj_m: AdjMatrix) -> bool:
    """
    Page 3, Q3 & Page 3, Q1 (Impact valuation).
    Vérifie si une matrice d'adjacence représente un graphe non orienté.
    La matrice doit être symétrique par rapport à la diagonale.
    """
    n = len(adj_m)
    for i in range(n):
        if len(adj_m[i]) != n:
            raise ValueError("La matrice n'est pas carrée.")
        for j in range(i + 1, n):
            # Pour un graphe non orienté, M[i][j] doit être égal à M[j][i]
            # Cela vaut aussi pour les poids (si pondéré).
            if adj_m[i][j] != adj_m[j][i]:
                return False
    return True

def al_is_undirected(adj_l: AdjLists) -> bool:
    """
    Page 4, Q2.
    Vérifie si des listes d'adjacence représentent un graphe non orienté.
    Pour tout arc u->v de poids w, il doit exister v->u de poids w.
    """
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
    """
    Page 4, Q3.
    Transforme un graphe orienté en non orienté en ajoutant les arcs réciproques manquants.
    Modifie le dictionnaire en place.
    """
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

def am_to_al(adj_m: AdjMatrix, vertices: Sequence[str] = ()) -> AdjLists:
    """
    Page 4, Q4.
    Convertit une matrice d'adjacence en listes d'adjacence.
    """
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
    """
    Page 4, Q4.
    Convertit des listes d'adjacence en matrice d'adjacence.
    """
    # On trie les sommets pour avoir un ordre déterministe (indices de matrice)
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


# =============================================================================
# EXERCICE 2 : Bibliothèque de manipulation de graphes
# =============================================================================

class Graph:
    """
    Page 4, Q1.
    Structure de données représentant un graphe simple, orienté ou non, pondéré ou non.
    """
    
    def __init__(self, directed: bool = False, weighted: bool = False):
        self.is_directed = directed
        self.is_weighted = weighted
        # Structure interne : Dictionnaire de dictionnaires pour accès O(1) aux poids
        # self.adj[u][v] = poids
        self.adj: Dict[str, Dict[str, int]] = {}

    @property
    def order(self) -> int:
        """Nombre de sommets."""
        return len(self.adj)

    @property
    def size(self) -> int:
        """Nombre d'arêtes/arcs."""
        count = 0
        for u in self.adj:
            count += len(self.adj[u])
        
        if not self.is_directed:
            # En non orienté, chaque arête est comptée deux fois (u->v et v->u)
            # Sauf les boucles (mais graphe simple ici)
            return count // 2
        return count

    def add_vertex(self, vertex: str):
        """Page 4, Q2: Ajouter un sommet."""
        if vertex not in self.adj:
            self.adj[vertex] = {}

    def remove_vertex(self, vertex: str):
        """
        Page 4, Q2: Supprimer un sommet.
        Entraîne la suppression des arêtes incidentes.
        """
        if vertex not in self.adj:
            return
        
        # Supprimer le sommet de la liste principale
        del self.adj[vertex]
        
        # Supprimer toutes les références à ce sommet chez les autres
        for u in self.adj:
            if vertex in self.adj[u]:
                del self.adj[u][vertex]

    def add_edge(self, u: str, v: str, weight: int = 1):
        """
        Page 4, Q2: Ajouter/Mettre à jour un arc/arête.
        Ajoute les sommets s'ils n'existent pas.
        """
        # Ajout des sommets manquants (effet secondaire demandé)
        self.add_vertex(u)
        self.add_vertex(v)
        
        actual_weight = weight if self.is_weighted else 1
        
        # Ajout u -> v
        self.adj[u][v] = actual_weight
        
        # Si non orienté, ajout v -> u
        if not self.is_directed:
            self.adj[v][u] = actual_weight

    def remove_edge(self, u: str, v: str):
        """Page 4, Q2: Supprimer un arc/arête."""
        if u in self.adj and v in self.adj[u]:
            del self.adj[u][v]
        
        if not self.is_directed:
            if v in self.adj and u in self.adj[v]:
                del self.adj[v][u]

    @classmethod
    def from_edge_list(cls, edges: List[Tuple[str, str, int]], vertices: Optional[List[str]] = None,directed: bool = False, weighted: bool = False) -> 'Graph':
        """
        Page 4, Q2: Créer un graphe à partir d'une liste d'arêtes.
        edges: liste de tuples (u, v, poids) ou (u, v)
        """
        g = cls(directed=directed, weighted=weighted)
        
        # Ajouter les sommets isolés éventuels
        if vertices:
            for v in vertices:
                g.add_vertex(v)
                
        for edge in edges:
            u, v = edge[0], edge[1]
            w = edge[2] if len(edge) > 2 else 1
            g.add_edge(u, v, w)
            
        return g

    def get_neighbors(self, u: str) -> List[str]:
        """Page 4, Q3: Donner le voisinage."""
        if u not in self.adj:
            return []
        return list(self.adj[u].keys())

    def degree(self, u: str) -> int:
        """Page 4, Q3: Calculer le degré."""
        if u not in self.adj:
            return 0
        
        if not self.is_directed:
            return len(self.adj[u])
        else:
            # En orienté : degré entrant + sortant
            out_degree = len(self.adj[u])
            in_degree = 0
            for v in self.adj:
                if u in self.adj[v]:
                    in_degree += 1
            return out_degree + in_degree

    def max_degree(self) -> int:
        """Page 4, Q3: Degré maximal du graphe."""
        if self.order == 0:
            return 0
        return max(self.degree(u) for u in self.adj)

    def density(self) -> float:
        """Page 4, Q3: Calculer la densité."""
        V = self.order
        E = self.size
        
        if V <= 1:
            return 0.0
            
        max_edges = V * (V - 1)
        if not self.is_directed:
            max_edges //= 2
            
        return E / max_edges

    def contract_edge(self, x: str, y: str):
        """
        Page 4, Q4: Contraction de l'arête (x, y).
        y est supprimé, fusionné dans x.
        Les poids conflictuels prennent la valeur minimale.
        """
        if x not in self.adj or y not in self.adj:
            return # Ou lever une erreur

        # 1. Rediriger les entrants : Tout z qui pointait vers y doit pointer vers x
        # Note : En non-orienté, c'est traité via la symétrie, mais on traite le cas général.
        nodes = list(self.adj.keys())
        for z in nodes:
            if z == y or z == x: continue
            
            # Si z pointe vers y
            if y in self.adj[z]:
                w_zy = self.adj[z][y]
                # Si z pointe déjà vers x, on prend le min
                if x in self.adj[z]:
                    self.adj[z][x] = min(self.adj[z][x], w_zy)
                else:
                    self.adj[z][x] = w_zy
                # On supprime le lien vers y plus tard via remove_vertex, 
                # mais pour la logique de poids, c'est fait.

        # 2. Transférer les sortants : Tout y -> z devient x -> z
        if y in self.adj:
            for z, w_yz in self.adj[y].items():
                if z == x: continue # On ignore l'auto-boucle créée par la contraction
                
                if z in self.adj[x]:
                    self.adj[x][z] = min(self.adj[x][z], w_yz)
                else:
                    self.adj[x][z] = w_yz
                    
        # 3. Si non orienté, s'assurer que la symétrie est respectée pour les nouveaux liens
        if not self.is_directed:
            for neighbor in self.adj[x]:
                self.adj[neighbor][x] = self.adj[x][neighbor]

        # 4. Supprimer y
        self.remove_vertex(y)


# =============================================================================
# ZONE DE TEST (Démonstration)
# =============================================================================
if __name__ == "__main__":
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

    print("\n--- Test Exercice 2 (Graph Class) ---")
    # Création graphe pondéré non orienté
    g = Graph(directed=False, weighted=True)
    g.add_edge("A", "B", 5)
    g.add_edge("B", "C", 10)
    g.add_edge("C", "A", 20)
    g.add_edge("C", "D", 4) # D sera ajouté auto
    
    print(f"Ordre: {g.order}, Taille: {g.size}") # Ordre 4, Taille 4
    print(f"Voisins de C: {g.get_neighbors('C')}")
    print(f"Degré de C: {g.degree('C')}") # Devrait être 3 (A, B, D)
    
    # Test Contraction: on contracte (C, D). C absorbe D.
    # L'arête C-D disparait. D disparait.
    print("\nContraction de l'arête (C, D)...")
    g.contract_edge("C", "D")
    
    print(f"Ordre après contraction: {g.order}") # 3 (A, B, C)
    print(f"Voisins de C après contraction: {g.get_neighbors('C')}") 
    # C garde ses liens avec A et B.
    
    # Test contraction avec conflit de poids
    # Ajoutons un nœud E relié à A (poids 2) et B (poids 8)
    g.add_edge("A", "E", 2)
    g.add_edge("B", "E", 8)
    
    # Si on contracte A et B (A mange B).
    # E était relié à A (2) et B (8). Le nouveau lien A-E doit être min(2, 8) = 2.
    # Le lien A-B (5) disparait. A hérite du lien B-C (10). A avait déjà A-C (20).
    # Nouveau lien A-C = min(10, 20) = 10.
    
    print("\nAvant contraction A-B:")
    print(f"Poids A-C: {g.adj['A']['C']}")
    print(f"Poids A-E: {g.adj['A']['E']}")
    print("Contraction A-B...")
    g.contract_edge("A", "B")
    
    print(f"Voisins de A: {g.adj['A']}")
    # Vérifications
    # A-C devrait être 10 (hérité de B-C qui était 10, vs ancien A-C 20)
    # A-E devrait être 2 (ancien A-E 2, vs ancien B-E 8)
    print(f"Poids final A-C (attendu 10): {g.adj['A']['C']}")
    print(f"Poids final A-E (attendu 2): {g.adj['A']['E']}")