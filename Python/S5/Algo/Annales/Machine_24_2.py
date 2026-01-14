"""
MOU possède une seule piste (atterissage ou décollage)
Qd MOU arrivé : ?
Qd MOU départ : num vol + type avion + nb passagers + nb crew + destination + h départ
Avions demandent droit à la tour --> rajoute aux autres demandes --> traiter rdre d'arrivée ca file
+ Capteur compte mouette au décollage ou atterrisssage
"""

##Logique d'une chaine pour pouvoir tout faire
import random
import time

# Listes prédéfinies pour l'initialisation
TYPES_AVIONS = ["Airbus A320", "Boeing 737", "Airbus A350", "ATR 72"]
DESTINATIONS = ["Nantes (NTE)", "Paris (CDG)", "Londres (LHR)", "Berlin (BER)"]

# ==========================================
# Q1 : Classe pour représenter un vol unique
# ==========================================
class Flight:
    def __init__(self, numero_vol, heure_prevue):
        # Données fournies 
        self.numero_vol = numero_vol
        self.heure = heure_prevue
        
        # Données aléatoires 
        self.type_avion = random.choice(TYPES_AVIONS)
        self.destination = random.choice(DESTINATIONS)
        self.passagers = random.randint(20, 150)
        self.equipage = random.randint(5, 10)
        self.mouettes = random.randint(0, 20)
        
        # Pointeur pour la liste chaînée 
        self.suivant = None

# ==========================================
# Q1-Q3 : Gestion des demandes (Liste/File)
# ==========================================
class Flights: #modif des fonctions de base selon énoncé
    def __init__(self):
        self.premier = None 

    # Q2 : Vérification et Affichage 
    def isEmpty(self):
        return self.premier is None

    def afficher(self):
        if self.isEmpty():
            print("Aucun vol en attente.")
            return
        courant = self.premier
        while courant:
            print(f"Vol {courant.numero_vol} | {courant.heure} | {courant.mouettes} mouettes | {courant.passagers} passagers")
            courant = courant.suivant

    # Q3 : Gestion de l'arrivée avec priorité 
    def ajouter_demande(self, nouveau_vol):
        # Cas 1 : Moins ou égal à 5 mouettes -> Fin de liste 
        if nouveau_vol.mouettes <= 5:
            if self.isEmpty():
                self.premier = nouveau_vol
            else:
                courant = self.premier
                while courant.suivant:
                    courant = courant.suivant
                courant.suivant = nouveau_vol
        
        # Cas 2 : Plus de 5 mouettes -> Prioritaire 
        else:
            # Calcul de la position : 20 mouettes = pos 1, 19 = pos 2... 
            position_cible = 21 - nouveau_vol.mouettes
            if position_cible == 1 or self.isEmpty():
                nouveau_vol.suivant = self.premier
                self.premier = nouveau_vol
            else:
                # On cherche à insérer à la position cible
                courant = self.premier
                index = 1
                while courant.suivant and index < position_cible - 1:
                    courant = courant.suivant
                    index += 1
                nouveau_vol.suivant = courant.suivant
                courant.suivant = nouveau_vol

    # Q4 : Correction récursive du nombre de mouettes 
    def corriger_mouettes_rec(self, noeud, soustraire=True):
        if noeud is None:
            return
        if soustraire:
            noeud.mouettes -= 2 # 1er, 3ème... on retire 2 
        else:
            noeud.mouettes += 2 # 2ème, 4ème... on ajoute 2 
        # Appel récursif pour le suivant avec inversion du signe
        self.corriger_mouettes_rec(noeud.suivant, not soustraire)

# ==========================================
# Q6 : Arbre Binaire 
# ==========================================

class NoeudArbre:
    def __init__(self, vol):
        self.vol = vol
        self.gauche = None
        self.droite = None

def inserer_arbre(racine, vol):
    if racine is None:
        return NoeudArbre(vol)
    # < 5 à gauche, = 5 racine, > 5 à droite 
    if vol.mouettes < 5:
        racine.gauche = inserer_arbre(racine.gauche, vol)
    elif vol.mouettes > 5:
        racine.droite = inserer_arbre(racine.droite, vol)
    # Note : si exactement 5, l'énoncé dit "dans la racine", 
    # donc on ne fait rien ou on traite selon la structure choisie.
    return racine

# ==========================================
# Q5 : Système de l'Aéroport et Tris
# ==========================================

import time

class Aeroport: #nouvelle classe pour plus simple, proposer par énoncé
    def __init__(self):
        self.gestionnaire_vols = Flights()

    def tri_bulle_manuel(self, liste_vols, critere): #tri choisi
        """
        Algorithme de tri à bulles manuel.
        Critères possibles : 'mouettes', 'passagers', 'heure'
        """
        n = len(liste_vols)
        for i in range(n):
            for j in range(0, n - i - 1):
                # getattr permet d'accéder dynamiquement à l'attribut (ex: vol.mouettes)
                val_actuelle = getattr(liste_vols[j], critere)
                val_suivante = getattr(liste_vols[j+1], critere)
                # Tri ascendant 
                if val_actuelle > val_suivante:
                    # Échange (Swap)
                    liste_vols[j], liste_vols[j+1] = liste_vols[j+1], liste_vols[j]
        return liste_vols

    def executer_et_mesurer_tris(self): #lance les tris
        # 1. Extraction des vols vers une liste temporaire 
        vols_a_trier = []
        courant = self.gestionnaire_vols.premier
        while courant:
            vols_a_trier.append(courant)
            courant = courant.suivant
        
        # 2. Liste des critères demandés par l'énoncé 
        criteres = ["mouettes", "passagers", "heure"]
        
        for crit in criteres:
            # Copie de la liste pour ne pas repartir d'une liste déjà triée
            copie_vols = list(vols_a_trier)
            
            # --- MESURE DU TEMPS ---
            debut = time.time() # Début du chrono
            
            self.tri_bulle_manuel(copie_vols, crit)
            
            fin = time.time() # Fin du chrono
            # -----------------------
            
            temps_execution = fin - debut # Calcul 
            print(f"Tri par {crit} terminé en {temps_execution:.8f} secondes.")