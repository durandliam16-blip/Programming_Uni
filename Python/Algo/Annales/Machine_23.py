"""
Pere noel s'adresse à un seul lutin, ils sont en grève.
Mess se transmet un par un.
Lutin possède (classe) prénom, age et niv audition (=nb de cara qu'il add ou supprime à un mess), nb kdo emballé et nb fabriqué
    Supprimera tjs les derniers cara et add les premiers au mess
    Cara choisi aléatoirement
    Cad O si aucune transfo
"""
from random import randint, random
from math import sqrt

#Q1 - Structure de données

class Lutins:
    def __init__(self, 
                prenom, age=100, 
                niv_audition=randint(-5, 5), 
                nb_emb=randint(0, 100), 
                nb_fab=randint(0, 100), 
                precedent=None, suivant=None):
        self.prenom = prenom
        self.age = age
        self.niv_audition = niv_audition
        self.nb_kdo_emballe = nb_emb
        self.nb_kdo_fabrique = nb_fab
        self.prev= precedent
        self.next= suivant

class Transmission:
    def __init__(self, premier, dernier=None):
        self.first = premier

#Q2 - Fonctions de base

    def isEmpty(self):
        if self.first is None:
            return True
        else:
            return False

    def afficher(self):
        current = self.first
        while current is not None:
            print(f"Lutin {current.prenom}, age {current.age}, niveau d'audition {current.niv_audition}, nombre de cadeaux emballés {current.nb_kdo_emballe}, nombre de cadeaux fabriqués {current.nb_kdo_fabrique}")
            current = current.next

#Q3 - Fonction de transmission

    def ajouter_lutin(self, nouveau: Lutins, cible_prenom, cible_age):
        if self.isEmpty(): #si vide, on le met comme 1er
            self.first = nouveau
            self.maj_ages()
            return
        courant = self.first
        while courant:
            if courant.prenom == cible_prenom and int(courant.age) == cible_age:
                nouveau.next = courant.next
                courant.next = nouveau
                self.maj_ages()
                return
            courant = courant.next

#Q4 - Nb parfaits

    def nbs_parfaits(self):
        parfaits = []
        courant = self.first
        while courant is not None:
            a = True
            somme_diviseurs = 0
            for i in range(1,courant.nb_fab):
                if courant.nb_fab % i == 0: #pour savoir si i divise val
                    somme_diviseurs += i
            if somme_diviseurs != courant.nb_fab:
                a = False
            somme_diviseurs = 0
            for i in range(1,courant.nb_emb):
                if courant.nb_emb % i == 0: #pour savoir si i divise val
                    somme_diviseurs += i
            if somme_diviseurs != courant.nb_emb:
                a = False
            if a == True:
                parfaits.append(courant.prenom)
        return parfaits

#Q5 - Calcul de pi

    def calcul_pi_rec(self, dernier_denominateur, produit_acc):
        # Calcul du nouveau dénominateur selon formule
        nouveau_denom = sqrt(2 + dernier_denominateur) 
        facteur = 2 / nouveau_denom 
        # Condition d'arrêt de l'énoncé 
        # Note: On utilise 1e15 pour 10^15
        if facteur <= (1 + 1e-15): #condition d'arret
            return produit_acc * facteur
        # Appel récursif 
        return self.calcul_pi_rec(nouveau_denom, produit_acc * facteur)

    def placement(self, bonhomme: Lutins):
            position = 1 # On commence à 1 pour le premier lutin [cite: 41]
            courant = self.first
            while courant is not None and courant != bonhomme:
                position += 1
                courant = courant.next
            return position

    def calcul_age(self, bonhomme: Lutins): #pas sur sur
        # On récupère la position via la méthode de l'instance
        pos = self.placement(bonhomme) 
        # On récupère la valeur de PI calculée récursivement [cite: 53]
        pi_val = self.calcul_pi() 
        # L'age = PI * position [cite: 41]
        bonhomme.age = pi_val * pos 
        return bonhomme.age

#Q6 - Resultat transmission 

    def transmettre(self, lutin : Lutins, message) -> str:
        if lutin is None: #verif si fin
            return message
        # Transformation du message
        n = lutin.niv_audition
        if n > 0: # Rajoute au début
            ajout = "".join(random.choice("abcdef") for _ in range(n))
            message = ajout + message
        elif n < 0: # Supprime à la fin
            message = message[:n] # n est négatif
        return self.transmettre(lutin.next, message)