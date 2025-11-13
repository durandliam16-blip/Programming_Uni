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
        courant = self.first
        i=0
        while courant != self.last:
            courant= courant.next
            i+=1
        return i+1
    #verif si vide
    def is_empty(self):
        return self.size == 0 

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
        if self.size == 1:
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
        if self.size == 1:
            self.first = self.last = None
        else:
            self.last = self.last.prev
            self.last.next = self.first
            self.first.prev = self.last
        return val

    #affiche bouts
    def see_first(self):
        return self.first.val
    def see_first(self):
        return self.last.val