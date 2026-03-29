""" Pour voir détails et autres def :
https://www.youtube.com/watch?v=SGf-BBtfP_w&list=WL&index=3&t=649s
"""

class Node:
    def __init__(self,data):
        self.item = data
        self.next = None 
        self.previous = None 

class List:
    def __init__(self):
        self.first=None
        self.last=None

    #Ajoute un noeud au début
    def add_first(self,item):
        node_item = Node(item) 
        node_item.next = self.first #l'ancien premier noeud
        self.first.previous = node_item #mtn noeud le precede
        self.first = node_item #devient premier
    
    #Ajoute un noeud spécifique au début
    def add_first_select(self, node : Node):
        node.next = self.first #mm logique
        self.first.previous = None 
        self.first = node

    #Ajoute un élem à la fin 
    def add_end(self, item):
        #Si liste vide, first et last pointent vers le meme 
        if self.first == None:
            self.first = Node(item) 
            self.last = self.first
        #Si la liste à un seul élem
        if self.first == self.last: #si premier est dernier
            self.last = Node(item) #ajoute notre noeud
            self.first.next = self.last #2 elem donc suivant est last
            self.last.previous = self.first #cad pointe vers self.first
        #Si plus d'un élem
        else: 
            current = Node(item) #instancie
            self.last.next = current #l'ajoute fin
            current.previous = self.last
            self.last = current

    #Noeud en para et non item
    def add_node(self, node): 
        #Si liste vide, first et last pointent vers le meme 
        if self.first == None:
            self.first = node 
            self.last = None
        #Si la liste à un seul élem
        if self.first == self.last: #si premier est dernier
            self.last = node #ajoute notre noeud
            self.first.next = self.last #2 elem donc suivant est last
            self.last.previous = self.first #cad pointe vers self.first
        #Si plus d'un élem
        else: 
            current = node #cad actuel dernier noeud pointe vers ce new noeud
            node.previous = self.last #new noeud pointe le précedent
            self.last.next = current #changer dernier noeud

    #insère élém à une place déf
    def insert(self, index, item):
        #si index negatif ou sup taille
        if index <0 or index > self.lenght():
            raise IndexError("mauvais index")
        #si correct
        else: 
            i=0
            node=self.first
            while i<index: #s'asssure select le bon en décalant au fu et à mesure
                i+=1
                node = node.next
            node_item = Node(item) #def notre noeud à insérer
            node_item.next = node #déplace le noeur trouver avec le while au suivant
            node.previous.next = node_item #remplace le suivant précedent de l'ancien node à cette place
            node_item.previous = node.previous #deplace le noeur precedent du noeur de base à derriere new noeur
            node.previous = node_item #remplace

    #recup noeud à l'index
    def get_node (self,index):
        #si liste vide ou index trop grand ou inf O
        if index <0 or self.lenght()==0 or index >= self.lenght() :
            raise IndexError("pb d'indice")
        else:
            #part deu début
            i= 0
            node = self.first
            while i < index:
                i +=1
                node = node.next
            return node
        
    #verif si vide
    def is_empty(self):
        return self.first == None
    #def la taille
    def lenght(self):
        node = self.first
        i=0
        while node is not None:
            node= node.next
            i+=1
        return i
    
    #peut facilement faire une def qui lit les nodes

    #supprime premier noeud
    def remove_first(self):
        #si vide
        if self.lenght()==0:
            raise IndexError("liste vide")
        #si un seul elem
        elif self.lenght()==1:
            self.first=None
            self.last=None
        #Sinon
        self.first = self.first.next #saute le noeud 
        self.first.previous = None #ref new premier noeud est None

    #supprime premier noeud
    def remove_first(self):
        #si vide
        if self.lenght()==0:
            raise IndexError("liste vide")
        #si un seul elem
        elif self.lenght()==1:
            self.first=None
            self.last=None
        #Sinon
        self.last = self.last.previous 
        self.last.next = None 

    #supprime selon index
    def pop(self,index):
        #si vide ou index sup taille
        if self.lenght()==0 or index<0 or index>self.lenght():
            raise IndexError("pb indice")
        #si un seul elem
        elif self.first==self.last:
            self.first=None
            self.last=None
        #si veut enelver premier
        elif index ==0:
            self.remove_first()
        #si veut enlever dernier
        elif index ==self.lenght()-1:
            self.remove_last()
        #Si normal
        else:
            i=0
            node=self.first
            while i < index:
                i+=1
                node=node.next
            node.previous.next=node.next
            node.next.previous=node.previous

if __name__ == "__main__":
    liste = List()
    liste.add_end(1)
    liste.add_end(2)
    liste.add_end(3)
    liste.add_end(4)
    liste.add_end(5)
    print("Taille :", liste.lenght()) #5
    liste.pop(2)
    print("Taille après pop 2 :", liste.lenght()) #4
    node = liste.get_node(2)
    print("Noeud à l'index 2 après pop :", node.item) #4