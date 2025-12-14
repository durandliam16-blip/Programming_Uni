class Cell: #Sert juste à initialiser cellule
    def __init__(self, valeur=None,precedent=None,suivant=None):
        self.val= valeur
        self.prev= precedent
        self.next= suivant

class Deque: #pour modifs et commandes
    def __init__(self,premier=None,dernier=None):
        self.first=premier
        self.last=dernier
        if self.first != None and self.last != None: 
            #def liaisons si pas vide
            self.first.next=self.last
            self.last.prev=self.first
            self.first.prev = self.last
            self.last.next = self.first

    #def la taille
    def size(self):
        if self.first is None:
            return 0
        courant = self.first
        i = 1
        while courant is not self.last:
            courant = courant.next
            i += 1
        return i
    #verif si vide
    def is_empty(self):
        return self.first is None

    #ajoute en premier
    def insert_debut(self, val):
        nouveau = Cell(val)
        if self.is_empty():
            nouveau.next = nouveau.prev = nouveau
            self.first = self.last = nouveau
        else:
            nouveau.next = self.first
            nouveau.prev = self.last
            self.first.prev = nouveau
            self.last.next = nouveau
            self.first = nouveau

    #ajoute en dernier
    def insert_fin(self, val):
        nouveau = Cell(val)
        if self.is_empty():
            nouveau.next = nouveau.prev = nouveau
            self.first = self.last = nouveau
        else:
            nouveau.prev = self.last
            nouveau.next = self.first
            self.last.next = nouveau
            self.first.prev = nouveau
            self.last = nouveau
    
    #Supprime et renvoie le premier
    def remove_first(self):
        if self.is_empty():
            raise IndexError("Suppression sur une liste vide")
        val = self.first.val
        if self.size() == 1:
            self.first = self.last = None
        else:
            self.first = self.first.next
            self.first.prev = self.last
            self.last.next = self.first
        return val
    
    #Supprime le dernier
    def remove_last(self):
        if self.is_empty():
            raise IndexError("Suppression sur une liste vide")
        val = self.last.val
        if self.size() == 1:
            self.first = self.last = None
        else:
            self.last = self.last.prev
            self.last.next = self.first
            self.first.prev = self.last
        return val

    #affiche bouts
    def see_first(self):
        return self.first.val
    def see_last(self):
        return self.last.val
    
if __name__ == "__main__":
    deque = Deque()
    deque.insert_fin(10)
    deque.insert_fin(20)
    deque.insert_debut(5)
    print("Taille :", deque.size())  # Taille : 3
    print("Premier élément :", deque.see_first())  # Premier élément : 5
    print("Dernier élément :", deque.see_last())    # Dernier élément : 20
    deque.remove_first()
    print("Premier élément après suppression :", deque.see_first())  # Premier élément après suppression : 10
    deque.remove_last()
    print("Dernier élément après suppression :", deque.see_last())    # Dernier élément après suppression : 10