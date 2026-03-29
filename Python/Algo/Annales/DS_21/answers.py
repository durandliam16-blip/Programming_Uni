##A - liste simplement chainée circulaire non vide

#A1 - Classes
class Node: #Classe de création de noeud
    def __init__(self, value, next=None):
        self.value = value      # entier stocké
        self.next = next        # maillon suivant
class List: #Classe de création de liste
    def __init__(self):
        self.last = None        # exo veut que dernier elem

#A2 - Affichage 
    def afficher(self) -> list: 
        if self.last is None: #penser verif vide
            print("Liste vide")
            return
        liste=[]
        courant=self.last.next #equivalent de self.first qd pas mis dans init
        while courant != self.last:
            liste.append(courant.value)
            courant=courant.next
        liste.append(self.last.value)
        return liste

#A3 - Ajout fin 
    def add_last(self, item):
        nouveau = Node(item) #Transforme valeur en noeud par classe
        if self.last is None: #verif liste vide
            nouveau.next = nouveau #pointe sur lui meme car liste vide
            self.last = nouveau #remplace le vide
        else:
            nouveau.next = self.last.next #car circulaire
            self.last.next = nouveau #ancien dernier pointe sur nouveau
            self.last = nouveau #mise a jour du dernier
#Complexité de 0(1) car pas de boucle, juste des affectations.

#A4 - Suppression 1er élem
    def suppr_last(self):
        if self.last is None: #si liste vide
            print("Impossible car liste vide")
            return
        first = self.last.next #récup le 1er élément
        if first == self.last: #si 1 seul élément
            self.last = None
        else: #si normal
            self.last.next = first.next #saute le 1er

#A5 - Tri par sélection
#Sur place donc pas d'ajouts ou d'autres structures ex liste ou tuple
    
    def tri_selection(self):
    #solution : échanger les valeurs des nœuds, pas les pointeurs
        if self.last is None: #si liste vide
            return
        start = self.last.next
        cur = start
        while True: #Remplace boucle en fonction de la taille
            # trouver minimum du segment restant
            mini = cur
            scan = cur.next
            while scan != start:
                if scan.value < mini.value:
                    mini = scan
                scan = scan.next
            # swap des valeurs
            cur.value, mini.value = mini.value, cur.value
            cur = cur.next #i+1
            if cur == start:
                break

##B - Calculs

#B - Nombre e 
def calcul_e(max):
    total = 0
    numerateur = 1
    denominateur = 1
    i = 1
    terme = numerateur / denominateur 
    while terme >= max:
        terme = numerateur / denominateur
        total += terme
        for i in range(1, i + 1):
            denominateur *= i
        i += 1
    return total

#B - Nombre parfaits

def nbs_parfaits(n):
    parfaits = []
    for k in range(1, n + 1):
        somme_diviseurs = 0
        for i in range(1, k): #pas +1 car pas k lui meme sinon fausse
            if k % i == 0: #pour savoir si i divise k
                somme_diviseurs += i
        if somme_diviseurs == k:
            parfaits.append(k)
    return parfaits

if __name__ == "__main__":
    print(calcul_e(1e-7))
    print(nbs_parfaits(10000))

##C - Arbres AVL

"""
Voici d'abord les règles de base d'un arbre AVL :
- Arbre Binaire de Recherche (ABR) : 
    Pour chaque nœud, les valeurs à gauche sont plus petites et les valeurs à droite sont plus grandes.
- Facteur d'Équilibre (FE) : 
    C'est la différence de hauteur entre le sous-arbre gauche et le sous-arbre droit (FE = hauteur(gauche) - hauteur(droite).
- Équilibre : Dans un AVL, le FE de chaque nœud doit être -1, 0 ou 1. 
    Si on obtient -2 ou 2, l'arbre est déséquilibré et on doit effectuer une rotation.
"""

#C1 - Placer 12
    #Sup 10 donc à sa droite mais désequilibre du FE de 50 donc rotation simple droite sur noeud 50
    #version finale en img 

#C2 - Placer 75 
    #A gauche de 80 mais 
    #Le déséquilibre est à la racine 100. Son fils gauche (50) a un FE de -1 (signe opposé). C'est un cas LR (Gauche-Droite). Il faut une Rotation Double.
        #Étape intermédiaire : Rotation gauche sur le nœud 50.
        #Étape finale : Rotation droite sur le nœud 100.
    """70 (FE:0)
          /    \
       50        100
      /  \      /    \
    20    60   80     200
   /          /         \
 10          75          300"""