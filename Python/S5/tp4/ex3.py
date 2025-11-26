"""Liste doublement chainée circulaire"""
class Cell: #Sert juste à initialiser cellule
    def __init__(self, valeur=None,precedent=None,suivant=None):
        self.val= valeur
        self.prev= precedent
        self.next= suivant
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

    def exchange(cell1 : Cell, cell2 : Cell, self) -> LinkedList:
        return LinkedList
    def topswoops(self) -> LinkedList
        #boucle
            #self.exchange(..,..,self)
            #print(liste)