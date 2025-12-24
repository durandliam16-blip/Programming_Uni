#Problème spécifique - Ex3
from __future__ import annotations
from typing import Optional, List, Any
import copy

class Cell:
    def __init__(self, value: int):
        self.value = value
        self.prev: Optional['Cell'] = None
        self.next: Optional['Cell'] = None
class LinkedList:
    def __init__(self):
        self.head: Optional['Cell'] = None
        self.size = 0
    def append(self, value: int):
        """Ajoute un élément en fin de liste 
            (pour construire la liste)."""
        new_cell = Cell(value)
        if self.size == 0:
            self.head = new_cell
            new_cell.next = new_cell
            new_cell.prev = new_cell
        else:
            tail = self.head.prev
            tail.next = new_cell
            new_cell.prev = tail
            new_cell.next = self.head
            self.head.prev = new_cell
        self.size += 1

    def to_list(self) -> List[int]:
        """Convertit la liste chaînée en liste Python standard pour affichage."""
        if self.size == 0:
            return []
        result = []
        curr = self.head
        for _ in range(self.size):
            result.append(curr.value)
            curr = curr.next
        return result

    # --- EXERCICE 3, QUESTION 1 : Inversion des k premiers éléments ---
    # [cite: 143, 144] "Ajouter ... une fonction d'inversion des k premiers éléments."
    def reverse_first_k(self, k: int):
        """Inverse les k premiers maillons de la liste circulaire."""
        if k <= 1 or k > self.size:
            return
        old_head = self.head
        # On avance jusqu'au k-ième élément, c'est lui qui deviendra la nouvelle tête
        current = self.head
        for _ in range(k - 1):
            current = current.next
        new_head = current
        # Le noeud qui suit le bloc à inverser (le (k+1)-ième)
        after_block = new_head.next 
        # Le noeud qui précède le bloc (la queue de la liste complète)
        tail = self.head.prev
        # --- Inversion des pointeurs à l'intérieur du bloc de k éléments ---
        curr = old_head
        for _ in range(k):
            # On échange next et prev pour chaque cellule du bloc
            temp = curr.next
            curr.next = curr.prev
            curr.prev = temp
            # On recule car 'prev' est devenu la direction vers l'avant logique du bloc inversé
            curr = temp # On passe au suivant (sens original)
        #les pointeurs internes sont inversés, il faut reconnecter les extrémités du bloc au reste de la liste circulaire.
        # 1. La nouvelle tête (new_head) est l'ancien k-ième élément.
        # Son 'prev' doit pointer vers la queue de la liste (tail).
        new_head.prev = tail
        tail.next = new_head # La queue pointe vers la nouvelle tête
        # 2. L'ancienne tête (old_head) est maintenant la fin du bloc inversé.
        # Son 'next' doit pointer vers 'after_block'.
        old_head.next = after_block
        after_block.prev = old_head
        # Mise à jour de la tête de liste
        self.head = new_head

#Q2
def generate_permutations(elements: List[int]) -> List[List[int]]:
    #une fonction qui énumère une à une, toutes les permutations
    """Génère toutes les permutations d'une liste d'entiers (récursif)."""
    if len(elements) <= 1:
        return [elements]
    perms = []
    # On prend le premier élément
    first = elements[0]
    # On génère les permutations du reste
    rest_perms = generate_permutations(elements[1:])
    #  "l'insertion de l'élément de tête à toutes les positions..."
    for p in rest_perms:
        for i in range(len(p) + 1):
            perms.append(p[:i] + [first] + p[i:])
    return perms

#Q3
def solve_topswops(n: int):
    #Résoudre le problème Topswops ... pour n dans [4,9]
    print(f"--- Résolution pour n={n} ---")
    # 1. Générer toutes les permutations de 1 à n
    initial_values = list(range(1, n + 1))
    all_perms = generate_permutations(initial_values)
    max_iterations = -1
    best_perm = []
    count_perms = 0
    total_perms = len(all_perms)
    for values in all_perms:
        # Création de la liste chaînée pour cette permutation
        # (On recrée l'objet pour ne pas modifier la référence de base)
        dll = LinkedList()
        for v in values:
            dll.append(v)
        iterations = 0
        # Simulation du jeu Topswops
        # Sécurité pour éviter les boucles infinies si n > grand
        while dll.head.value != 1 and iterations < 1000:
            k = dll.head.value
            dll.reverse_first_k(k)
            iterations += 1
        if iterations > max_iterations:
            max_iterations = iterations
            best_perm = values
    print(f"Nombre maximum d'itérations trouvées : {max_iterations}")
    print(f"Permutation record : {best_perm}")
    return max_iterations, best_perm

if __name__ == "__main__":
    # Note : Le code va chercher LE maximum (qui peut être 10 ou plus pour n=6)
    solve_topswops(6)