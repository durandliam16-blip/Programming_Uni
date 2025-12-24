from typing import Any, Optional

#Deque basique comme Ex4
#Est utilisé par deux autres classes
class Deque:
    def __init__(self):
        self._items = [] 
    def is_empty(self) -> bool:
        return len(self._items) == 0
    def add_tail(self, item: Any):
        self._items.append(item)
    def add_head(self, item: Any):
        self._items.insert(0, item)
    def remove_tail(self) -> Optional[Any]:
        if self.is_empty(): return None
        return self._items.pop()
    def remove_head(self) -> Optional[Any]:
        if self.is_empty(): return None
        return self._items.pop(0)

#Ex6
class Stack:
    """
    Implémentation d'une PILE (LIFO - Last In First Out) via un Deque.
    On entre et on sort du MÊME côté.
    """
    def __init__(self):
        # Composition : La Stack "possède" un Deque
        self._container = Deque() 
        #permet d'utiliser fonctions deja def en réutilisant self._container
    def is_empty(self) -> bool:
        return self._container.is_empty()
    def push(self, item: Any):
        """Empiler : Ajout en queue du dèque."""
        self._container.add_tail(item)
    def pop(self) -> Optional[Any]:
        """Dépiler : Retrait en queue du dèque (le dernier ajouté)."""
        return self._container.remove_tail()
    def peek(self) -> Optional[Any]:
        """Regarder le sommet sans dépiler."""
        if self.is_empty(): return None
        # On retire et on remet (ou on accède directement si le Deque le permet)
        val = self._container.remove_tail()
        self._container.add_tail(val)
        return val

class Queue:
    """
    Implémentation d'une FILE (FIFO - First In First Out) via un Deque.
    On entre d'un côté et on sort de l'OPPOSÉ.
    """
    def __init__(self):
        self._container = Deque()
    def is_empty(self) -> bool:
        return self._container.is_empty()
    def enqueue(self, item: Any):
        """Enfiler : Ajout en queue."""
        self._container.add_tail(item)
    def dequeue(self) -> Optional[Any]:
        """Défiler : Retrait en TÊTE (le plus ancien)."""
        return self._container.remove_head()
    def front(self) -> Optional[Any]:
        """Regarder le premier élément."""
        if self.is_empty(): return None
        val = self._container.remove_head()
        self._container.add_head(val) # On remet immédiatement
        return val

"""La nouveauté, c'est que tu n'écris aucune logique algorithmique dans l'exercice 6. 
Tu ne fais que "brancher" des fils pour relier Stack.push à Deque.add_tail. 
C'est de l'assemblage (utilisant Deque), plus de la fabrication."""

#Programme de test
if __name__ == "__main__":
    print("--- Test de la PILE (Stack) ---")
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    print(f"J'ai empilé 1, 2, 3.")
    print(f"Pop 1 (attendu 3) : {s.pop()}")
    print(f"Pop 2 (attendu 2) : {s.pop()}")
    print(f"Pop 3 (attendu 1) : {s.pop()}")
    # Si l'ordre est inverse à l'insertion -> C'est bien une Pile.

    print("\n--- Test de la FILE (Queue) ---")
    q = Queue()
    q.enqueue("A")
    q.enqueue("B")
    q.enqueue("C")
    print(f"J'ai enfilé A, B, C.")
    print(f"Dequeue 1 (attendu A) : {q.dequeue()}")
    print(f"Dequeue 2 (attendu B) : {q.dequeue()}")
    print(f"Dequeue 3 (attendu C) : {q.dequeue()}")
    # Si l'ordre est identique à l'insertion -> C'est bien une File.