from __future__ import annotations
from typing import Optional, List

#Q1
def max_naive(nums: List[int], k: int) -> List[int]:
    taille = len(nums)
    if taille * k == 0:
        #verif taille et int en meme temps
        return []
    resultats = []
    for i in range(taille - k + 1):
        #Extrait la sous-séquence
        fenetre = nums[i : i + k] #remplace la 2ème boucle
        #Prend le max 
        resultats.append(max(fenetre))
    return resultats

#Q2

#Implémentation du Dèque, le visuel avec comandes simples
class Deque:
    def __init__(self):
        self._data = LinkedList()
    def is_empty(self) -> bool:
        return self._data.is_empty()
    def push_back(self, item: int):
        """Ajoute un élément en queue."""
        self._data.add_tail(item)
    def pop_front(self) -> Optional[int]:
        """Retire et renvoie l'élément de tête."""
        return self._data.remove_head()
    def pop_back(self) -> Optional[int]:
        """Retire et renvoie l'élément de queue."""
        return self._data.remove_tail()
    def peek_front(self) -> Optional[int]:
        """Regarde la valeur en tête sans la retirer."""
        return self._data.get_head_value()
    def peek_back(self) -> Optional[int]:
        """Regarde la valeur en queue sans la retirer."""
        return self._data.get_tail_value()
    
#Implémentation de la liste, l'arrière avec le détail
class Cell:
    def __init__(self, value: int):
        self.value = value
        self.prev: Optional['Cell'] = None
        self.next: Optional['Cell'] = None
class LinkedList:
    def __init__(self):
        self.head: Optional['Cell'] = None
        self.size = 0
    def is_empty(self) -> bool:
        return self.size == 0
    def add_tail(self, value: int):
        new_cell = Cell(value)
        if self.is_empty():
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
    def remove_head(self) -> Optional[int]:
        if self.is_empty():
            return None
        value = self.head.value
        if self.size == 1:
            self.head = None
        else:
            tail = self.head.prev
            new_head = self.head.next
            tail.next = new_head
            new_head.prev = tail
            self.head = new_head
        self.size -= 1
        return value
    def remove_tail(self) -> Optional[int]:
        if self.is_empty():
            return None
        tail = self.head.prev
        value = tail.value
        if self.size == 1:
            self.head = None
        else:
            new_tail = tail.prev
            new_tail.next = self.head
            self.head.prev = new_tail
        self.size -= 1
        return value
    def get_head_value(self) -> Optional[int]:
        return self.head.value if self.head else None
    def get_tail_value(self) -> Optional[int]:
        return self.head.prev.value if self.head else None
    
#REPONSE
def max_custom(nums: List[int], k: int) -> List[int]:
    if not nums or k == 0:
        return []
    # On instancie NOTRE Deque personnalisé
    d = Deque()
    resultats = []
    for i in range(len(nums)):

        # 1. Nettoyage à gauche (Tête)
        # On regarde si l'indice en tête (le plus vieux) est sorti de la fenêtre.
        # La fenêtre valide va de [i - k + 1] à [i].
        if not d.is_empty() and d.peek_front() <= i - k:
            d.pop_front()
        
        # 2. Nettoyage à droite (Queue) - Le principe "Monotonic Queue"
        # Si la valeur actuelle (nums[i]) est plus grande que la valeur correspondant
        # à l'indice stocké en queue du dèque, cet indice en queue ne sert plus à rien.
        # (Il est plus petit ET plus vieux que nums[i], il ne sera jamais le max).
        while not d.is_empty() and nums[d.peek_back()] < nums[i]:
            d.pop_back()
        
        # 3. Ajouter l'indice courant et enregistrer le result
        d.push_back(i)
        # Le maximum est toujours l'indice stocké en TÊTE du dèque.
        if i >= k - 1:
            indice_max = d.peek_front()
            resultats.append(nums[indice_max])
    return resultats


"""
Version Naïve :
    Pour chaque élément (environ N), on parcourt la fenêtre de taille K.
    Complexité : O(N*K).
    Si K est grand (ex: N/2), c'est très lent (O(N**2)).
Version Dèque :
    Chaque élément est ajouté une seule fois au dèque et retiré au plus une fois.
    Les opérations sur le dèque (push/pop) sont en O(1).
    Complexité : O(N). C'est une amélioration majeure, l'algorithme est linéaire quelle que soit la taille de la fenêtre.
"""

if __name__ == "__main__":
    liste_test = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    print(f"Liste : {liste_test}, k={k}")
    res = max_custom(liste_test, k)
    print(f"Max glissants : {res}")