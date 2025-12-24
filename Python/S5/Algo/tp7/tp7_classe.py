# =============================================================================
# EXERCICE 2 : Bibliothèque de manipulation de graphes
# =============================================================================

from typing import Dict, List, Tuple, Optional

class Graph:
    """Structure de données représentant un graphe simple, orienté ou non, pondéré ou non."""
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
        """Ajouter un sommet."""
        if vertex not in self.adj:
            self.adj[vertex] = {}

    def remove_vertex(self, vertex: str):
        """Supprimer un sommet.
        Entraîne la suppression des arêtes incidentes."""
        if vertex not in self.adj:
            return
        # Supprimer le sommet de la liste principale
        del self.adj[vertex]
        # Supprimer toutes les références à ce sommet chez les autres
        for u in self.adj:
            if vertex in self.adj[u]:
                del self.adj[u][vertex]

    def add_edge(self, u: str, v: str, weight: int = 1):
        """Ajouter/Maj un arc/arête.
        Ajoute les sommets s'ils n'existent pas."""
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
        """Supprimer un arc/arête."""
        if u in self.adj and v in self.adj[u]:
            del self.adj[u][v]
        if not self.is_directed:
            if v in self.adj and u in self.adj[v]:
                del self.adj[v][u]

    @classmethod
    def from_edge_list(cls, edges: List[Tuple[str, str, int]], vertices: Optional[List[str]] = None,directed: bool = False, weighted: bool = False) -> 'Graph':
        """Créer un graphe à partir d'une liste d'arêtes.
        edges: liste de tuples (u, v, poids) ou (u, v)"""
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
        """Donner le voisinage."""
        if u not in self.adj:
            return []
        return list(self.adj[u].keys())

    def degree(self, u: str) -> int:
        """Calculer le degré."""
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
        """Degré maximal du graphe."""
        if self.order == 0:
            return 0
        return max(self.degree(u) for u in self.adj)

    def density(self) -> float:
        """Calculer la densité cad le rapport entre nb d'arêtes divisé par nb d'arêtes possibles."""
        V = self.order
        E = self.size
        if V <= 1:
            return 0.0
        max_edges = V * (V - 1)
        if not self.is_directed:
            max_edges //= 2
        return E / max_edges

    def contract_edge(self, x: str, y: str):
        """Contraction de l'arête (x, y).
        y est supprimé, fusionné dans x.
        Les poids conflictuels prennent la valeur minimale."""
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