"""
Supercam sur le Perseverance
Cherche à gérer les roches sélectionnées par la cam
Classe roche : dureté (1 à 10), texture (cara), dilatation (1 à 10),
    poids, diametre max et la couleur
3 tubes de stockage de roches à dispo selon diametre max 
    1 jusqua 10cm, 2 entre 10 et 30cm et le 3 pour plus de 30
Perseverance fait 2 choses : 
    1. sélectionner et recup les roches (choix tubes)
    2. analyse des rochers (choix tube aléatoire puis systeme de pile)
"""
##Parfait exemple de mélange de classes
##Attention devrait etre files au lieu de piles

import random

#Q1 - Structure de données

class Tube:
    def __init__(self):
    #nécessaire pour les classes
        self.items = [] #pour l'objet actuel items = liste vide
    def push(self, val):
        self.items.append(val)
    def pop(self):
        if not self.isEmpty():
            return self.items.pop(-1) #haut pile
        raise IndexError("La pile est vide")
    def top(self):
        if not self.isEmpty():
            return self.items[-1]
        raise IndexError("La pile est vide") 
    def isEmpty(self):
        return len(self.items) == 0
    def size(self):
        return len(self.items)

class Perseverance:
    def __init__(self):
        #Ex de classe dans init d'autre classe
        self.tube1 = Tube() #jusqua 10cm 
        self.tube2 = Tube() #10-30cm
        self.tube3 = Tube() #plus de 30cm
        self.origine1 = Tube() 
        self.origine2 = Tube()
        self.origine3 = Tube() 
        self.origine4 = Tube() 

#Q2 - Nouvelles fonctions 

    def stocker_roche(self, roche):
        diametre = roche['diametre'] #dico idéale !!
        #le type de roche est un dict, ex {'diametre': 15, ...}
        if diametre <= 10:
            self.tube1.push(roche)
        elif 10 < diametre <= 30:
            self.tube2.push(roche)
        else:
            self.tube3.push(roche)

    def affichage_tubes(self):
        print("Tube 1 :", self.tube1.items)
        print("Tube 2 :", self.tube2.items)
        print("Tube 3 :", self.tube3.items)
        #car self.tubex equivaut à Tube() donc peut use .items

    def verif_tubes(self):
        #utilise fonction pile qui use len
        if self.tube1.isEmpty == True:
            print("premier vide")
        if self.tube2.isEmpty == True:
            print("second vide")
        if self.tube3.isEmpty == True:
            print("troisième vide")

#Q3 - Tache 2
    def analyser_roche(self):
        tube_choice = random.choice([self.tube1, self.tube2, self.tube3])
        #commande pour choix parmis options
        if self.tube_choice.isEmpty == True:
            self.analyser_roche(self)
        else: 
            roche = self.tube_choice.items.pop()
            produit = roche['durete']*roche['dilatation']
            if 1 <= produit <= 10:
                print("magmatique")
                self.origine1.push(roche)
            elif 10 < produit <= 20:
                print("metamorphique")
                self.origine2.push(roche)
            elif 20 < produit <= 50:
                print("sedimentaire")
                self.origine3.push(roche)
            elif 50 < produit <= 100:
                print("biogenique")
                self.origine4.push(roche)

#Q4 - Pb particulier 

    def verif_magmatique(self):
        n = len(self.origine1.items)
        for i in range (n):
            roche = self.origine1.items.pop()
            produit = roche['durete']*roche['dilatation']
            if 1 <= produit <= 10:
                pass
            else: 
                print(roche, "est mal placée")

#Q5 - Verif palindrome

#Q6 - Arbre bianire

from typing import ClassVar
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

P = Perseverance()
tube = P.tube2.items
poids=[]
for vals in tube:
    poids.append(vals['poids'])
#boucle et dico pour verif pas de doublons
abr = Arbre(nodes=poids)
print(abr.lookup_rec())
