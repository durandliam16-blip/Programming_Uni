"""Liste doublement chainée circulaire"""

##Ex1 
#Q1
class Cell: #Sert juste à initialiser cellule
    def __init__(self, valeur=None,precedent=None,suivant=None):
        self.val= valeur
        self.prev= precedent
        self.next= suivant

#Q2
class LinkedList: #pour modifs et commandes
    def __init__(self,premier=None,dernier=None):
        self.first=premier
        self.last=dernier
        if self.first != None and self.last != None: 
            #def liaisons si pas vide
            self.first.next=self.last
            self.last.prev=self.first
            self.first.prev = self.last
            self.last.next = self.first

    #Q3
    #verif si vide
    def is_empty(self):
        return self.size == 0
    #def la taille
    def size(self):
        courant = self.first
        i=0
        while courant != self.last:
            courant= courant.next
            i+=1
        return i+1
    #renvoie le premier
    def head(self):
        return self.first
    def tail(self):
        return self.last

##Ex2
    #Q1
    #insère à place déf
    def insert(self, item: int, neighbor: Cell, after: bool = True) -> LinkedList:
        courant=self.first
        while courant != neighbor: 
        #s'asssure select le bon en décalant au fur et à mesure
            courant = courant.next
        if courant.next == self.first: 
        #verif pas dernier
            after = False
        if after==True:
            nouveau = Cell(item)
            suivant = courant.next
            # insérer entre courant et suivant
            courant.next = nouveau
            nouveau.prev = courant
            nouveau.next = suivant
            suivant.prev = nouveau
        else: 
            nouveau = Cell(item)
            precedent = courant.prev
            # insérer entre previous et courant
            courant.prev = nouveau
            nouveau.next = courant
            nouveau.prev = precedent
            precedent.next = nouveau
        return False 

    #Q2
    #nouvelle fin
    def insert_first(self, item):
        nouveau = Cell(item) 
        nouveau.next = self.first #l'ancien premier noeud
        self.first.prev = nouveau #mtn noeud le precede
        self.first = nouveau #devient premier
    #nouvelle tete
    def insert_fin(self, item):
        nouveau = Cell(item) 
        nouveau.prev = self.last #l'ancien premier noeud
        self.last.next = nouveau #mtn noeud le precede
        self.last = nouveau #devient premier

    #Q3 - afficher liste
    def __str__(self) -> str : 
        liste=[]
        courant=self.first
        while courant != self.last:
            liste.append(courant.val)
            courant=courant.next
        print(liste)

    #Q4 - verif debut et fin lié et pas vide
    def isChained(self) -> bool:
        if (self.last.next != self.first) or (self.first.prev != self.last) or (self.size == 0):
            return False
        else:
            return True
    
    #Q5
    #trouve indice
    def find (self, item: int):
        i=0
        courant = self.first
        while courant.val != item:
            i+=1 
            courant = courant.next
            if i > self.size(self):
                return None
        print("indice : ",i)
    #trouve cell
    def findAt(i: int, self) -> Cell:
        y=0
        courant=self.first
        while y != i:
            y+=1
        return courant
    
    #Q6
    #trouve élem
    def getValue(self,idx: int) -> int:
        y=0
        courant=self.first
        while y != idx:
            y+=1
        return courant.val
    #remplacer valeur
    def setValue(self, idx: int, item: int) -> LinkedList:
        y=0
        courant=self.first
        while y != idx:
            y+=1
        courant.val = item
        return self

    #Q7 - supprimer une cellule
    def remove(self, cell : Cell) -> LinkedList:
        courant=self.first
        while courant != cell:
            courant=courant.next
        courant.prev.next=courant.next
        courant.next.prev=courant.prev
    
    #Q8 - concatène deux listes (liste fin de self)
    def extend(self, liste: LinkedList) -> LinkedList:
        self.last.next = liste.first
        liste.last.prev = self.last
        liste.last.next = self.first
        self.first.prev = liste.last
        return self