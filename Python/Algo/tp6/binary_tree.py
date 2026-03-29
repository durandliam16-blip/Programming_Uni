##Ex1
from typing import ClassVar

#Q1
class Noeud:
    def __init__(self, valeur, g: 'Noeud' = None, d: 'Noeud' = None) -> None:
        self.val = valeur
        # children: gauche (g) et droite (d)
        self.g = g
        self.d = d


class Arbre:
    # renvoyer un terminal unique au lieu de None
    terminal: ClassVar[Noeud] = Noeud(None)
    terminal.g = terminal
    terminal.d = terminal

    #Q3 - constructeur correct
    def __init__(self, rac: Noeud | None = None, nodes: list[int | None] | None = None) -> 'Arbre':
        if nodes is not None:
            built = self.make_tree(nodes)
            self.racine = built.racine
        else:
            if isinstance(rac, Noeud):
                self.racine = rac
                # normalize None children to terminal sentinel
                def _norm(node: Noeud):
                    if node is Arbre.terminal:
                        return
                    if node.g is None:
                        node.g = Arbre.terminal
                    else:
                        _norm(node.g)
                    if node.d is None:
                        node.d = Arbre.terminal
                    else:
                        _norm(node.d)

                _norm(self.racine)
            else:
                # si rac est None ou non fourni -> arbre vide (terminal)
                self.racine = Arbre.terminal

    def make_tree(self, nodes: list[int | None]) -> 'Arbre':
        # Crée la liste de noeuds (ou terminal pour None)
        node_list: list[Noeud] = []
        for val in nodes:
            if val is None:
                node_list.append(Arbre.terminal)
            else:
                node_list.append(Noeud(val))

        # Définit les relations g/d (gauche/droite)
        for i in range(len(node_list)):
            if node_list[i] is Arbre.terminal:
                continue
            left_index = 2 * i + 1
            right_index = 2 * i + 2
            node_list[i].g = node_list[left_index] if left_index < len(node_list) else Arbre.terminal
            node_list[i].d = node_list[right_index] if right_index < len(node_list) else Arbre.terminal

        return Arbre(node_list[0])

    # parcours en profondeur préfixe (préordre)
    def affpre(self) -> None:
        def _rec(node: Noeud):
            if node is Arbre.terminal:
                return
            print(node.val)
            _rec(node.g)
            _rec(node.d)

        _rec(self.racine)

    #Q2
    def isEmpty(self) -> bool:
        return self.racine is Arbre.terminal

    def root(self) -> object:
        return None if self.racine is Arbre.terminal else self.racine.val

    def terminal2(self) -> Noeud:
        return Arbre.terminal

    #Q4
    def height(self) -> int:
        def height_tree(node: Noeud) -> int:
            if node is Arbre.terminal:
                return 0
            return 1 + max(height_tree(node.g), height_tree(node.d))

        return height_tree(self.racine)

    def size(self) -> int:
        def size_tree(node: Noeud) -> int:
            if node is Arbre.terminal:
                return 0
            return 1 + size_tree(node.g) + size_tree(node.d)
        return size_tree(self.racine)



    ## --- Exercice 4: Arbres binaires de recherche ---
    """
    toutes les clés du sous-arbre gauche de x sont inférieures—ou égales—à la clé de x ;
    toutes les clés du sous-arbre droit de x sont supérieures à la clé de x.
    """
    #Q1
    def isBst(self) -> bool:
        """Q1: Vérifie si l'arbre respecte la propriété d'ABR."""
        def _check(node: Noeud, min_val: float, max_val: float) -> bool:
            # Si on atteint un terminal, c'est valide
            if node is Arbre.terminal:
                return True
            # La valeur doit être comprise entre les bornes
            if not (min_val < node.val <= max_val):
                return False
            # On récurre à gauche (maj borne max) et à droite (maj borne min)
            return (_check(node.g, min_val, node.val) and 
                    _check(node.d, node.val, max_val))
        return _check(self.racine, float('-inf'), float('inf'))

    #Q2
    def lookup_rec(self, key: int) -> Noeud:
        """Q2: Recherche récursive d'une clé."""
        def _rec(node: Noeud, k: int) -> Noeud:
            # Non trouvé ou trouvé
            if node is Arbre.terminal or node.val == k:
                return node
            # Direction gauche ou droite selon la valeur
            if k < node.val:
                return _rec(node.g, k)
            return _rec(node.d, k)
        return _rec(self.racine, key)

    def lookup_it(self, key: int) -> Noeud:
        """Q2: Recherche itérative (boucle while)."""
        curr = self.racine
        while curr is not Arbre.terminal and curr.val != key:
            if key < curr.val:
                curr = curr.g
            else:
                curr = curr.d
        return curr

    #Q3
    def insert(self, key: int) -> 'Arbre':
        """Q3: Insertion d'une clé (sans doublons)."""
        def _ins(node: Noeud, k: int) -> Noeud:
            if node is Arbre.terminal:
                return Noeud(k, Arbre.terminal, Arbre.terminal)
            if k < node.val:
                node.g = _ins(node.g, k)
            elif k > node.val:
                node.d = _ins(node.d, k)
            # Si k == node.val, on ne fait rien (pas de doublons)
            return node
        self.racine = _ins(self.racine, key)
        return self

    #Q4
    def remove(self, key: int) -> 'Arbre':
        """Q4: Supprime la clé key de l'ABR en maintenant la structure."""
        
        def _min_value_node(node: Noeud) -> Noeud:
            """Trouve le nœud avec la plus petite valeur dans un sous-arbre."""
            current = node
            while current.g is not Arbre.terminal:
                current = current.g
            return current

        def _delete(node: Noeud, k: int) -> Noeud:
            if node is Arbre.terminal:
                return Arbre.terminal
            # Étape 1 : Rechercher le nœud à supprimer
            if k < node.val:
                node.g = _delete(node.g, k)
            elif k > node.val:
                node.d = _delete(node.d, k)
            else:
                # Étape 2 : On a trouvé le nœud !
                # Cas A : Le nœud a 0 ou 1 enfant
                if node.g is Arbre.terminal:
                    return node.d
                elif node.d is Arbre.terminal:
                    return node.g
                # Cas B : Le nœud a 2 enfants
                # On cherche le successeur (le plus petit du côté droit)
                temp = _min_value_node(node.d)
                # On remplace la valeur actuelle par celle du successeur
                node.val = temp.val
                # On supprime le successeur dans le sous-arbre droit
                node.d = _delete(node.d, temp.val)
            return node
        self.racine = _delete(self.racine, key)
        return self


## --- Exercice 5: Conversion vers Liste Doublement Chaînée ---

    def toList(self) -> 'Noeud':
        """
        Convertit l'ABR en une liste circulaire doublement chaînée.
        Retourne le premier élément (le plus petit).
        """
        def _join(a: Noeud, b: Noeud) -> Noeud:
            """Relie deux listes circulaires entre elles."""
            if a is Arbre.terminal: return b
            if b is Arbre.terminal: return a
            # Récupère les derniers éléments de chaque liste
            a_last = a.g
            b_last = b.g
            # Connecte la fin de a avec le début de b
            a_last.d = b
            b.g = a_last
            # Connecte la fin de b avec le début de a (circularité)
            b_last.d = a
            a.g = b_last
            return a

        def _convert(node: Noeud) -> Noeud:
            if node is Arbre.terminal:
                return Arbre.terminal
            # Récurrence sur les deux fils
            L_gauche = _convert(node.g)
            L_droite = _convert(node.d)
            # Transformer le nœud actuel en une liste de 1 élément circulaire
            node.g = node
            node.d = node
            # Assembler : Gauche + Courant + Droite
            res = _join(L_gauche, node)
            res = _join(res, L_droite)
            return res
        return _convert(self.racine)


if __name__ == "__main__":

    #Constru manuelle
    a = Arbre(Noeud("x",
                Noeud("/", Noeud("x"), Noeud("-", Noeud("x"), Noeud(1))),
                Noeud("+", Noeud(78), Noeud("y"))))
    arb = Arbre()
    a.affpre()
    print(a.root())

    #Constru auto
    BinaryTree = Arbre()
    t = [2, 1, 4, 0, None, 3, 5]
    bt = BinaryTree.make_tree(t)
    print(bt.height())
    print(bt.size())


    # --- TEST EXERCICE 4 (ABR) ---
    print("--- Test Exercice 4: Arbre Binaire de Recherche ---")
    
    # Création de l'arbre de la Figure 3
    # Valeurs: [6, 2, 11, 1, 4, 7, 12, None, None, 3, None, None, None, 12, 14]
    t_abr = [6, 2, 11, 1, 4, 7, 12, None, None, 3, None, None, None, 12, 14]
    abr = Arbre(nodes=t_abr)
    
    print(f"L'arbre est-il un ABR ? {abr.isBst()}") # Attendu: True
    
    # Test de recherche (Lookup)
    n_7 = abr.lookup_it(7)
    print(f"Recherche de 7: {'Trouvé' if n_7 is not Arbre.terminal else 'Non trouvé'}")
    
    n_99 = abr.lookup_rec(99)
    print(f"Recherche de 99: {'Trouvé' if n_99 is not Arbre.terminal else 'Non trouvé'}")

    # Test d'insertion
    print("Insertion de 5...")
    abr.insert(5)
    print(f"Taille après insertion: {abr.size()}") # Devrait augmenter de 1

    # Test de suppression (Q4)
    print("Suppression de 11 (nœud avec deux enfants)...")
    abr.remove(11)
    print(f"11 est-il encore là ? {abr.lookup_it(11) is not Arbre.terminal}")

    # --- TEST EXERCICE 5 (LISTE) ---
    print("\n--- Test Exercice 5: Conversion en Liste ---")
    
    # On calcule d'abord la taille (toList mutera l'arbre)
    n = abr.size()
    # On convertit notre ABR actuel en liste (opération en-place)
    tete_liste = abr.toList()

    # Pour vérifier, on parcourt la liste avec le pointeur .d (suivant)
    # Comme c'était un ABR, les valeurs doivent sortir dans l'ordre croissant
    print("Parcours de la liste (via .d) :")
    curr = tete_liste
    for _ in range(n):
        print(curr.val, end=" -> ")
        curr = curr.d
    print("RETOUR AU DÉBUT (Circulaire)")