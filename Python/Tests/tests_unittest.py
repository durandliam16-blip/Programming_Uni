"""
Tests unittest à faire (verif les fonctionnalitées de base): 
(- taille grille lors de la création)
- nb voisins, avec matrice 3x3
- changement état par 1 cellule puis globalement
- forme matrice initiale, basique
(- imprime diff)
"""

import unittest
from mainV1 import *

class TestIncremente(unittest.TestCase):
    
    def test_voisins(self):
        M=[[0,0,0],[1,1,1],[0,1,0]]
        self.assertEqual(nbVoisins(M,1,1), 3)

    def many_test_voisins(self):
        mes_tests = []
        M = [[0, 0, 0],[0, 1, 0],[0, 0, 0]]
        mes_tests.append((M,0))
        etapes = [(2,1),(1,0),(0,1),(1,2)] 
        #Boucle qui ajoute un voisin à chaque étapes:
        for ligne, colonne in etapes:
            #Si déjà un voisin on passe
            if M[ligne][colonne] == 0:
                M[ligne][colonne] = 1
                nb_voisins += 1
            M_new = [ligne.copy() for ligne in M]
            mes_tests.append((M_new, nb_voisins))
        for value_in, value_out in mes_tests:
            with self.subTest(value_in=value_in, value_out=value_out):
                self.assertEqual(nbVoisins(value_in), value_out)

    def test_changement_etat_simple(self):
        M = [[0,0,0],[0,1,0],[0,0,0]]
        M_next = [[0,0,0],[0,0,0],[0,0,0]]
        self.assertEqual(ChangeEtat(M),M_next)

    def test_changement_etat_complexe(self):
        M = [[0,1,0],[0,0,1],[0,1,0]]
        M_next = [[0,0,0],[0,1,0],[0,0,0]]
        self.assertEqual(ChangeEtat(M),M_next)
    
    def test_forme(self):
        taille=4
        M=ConfigInit(taille)
        self.assertEqual(len(M), taille+2)

    def many_test_forme(self):
        mes_tests = []
        for taille in range(1,10):
            M=ConfigInit(taille)
            mes_tests.append((M, taille+2)) #Car créer bordure à ConfigInit dans mon code
        for value_in, value_out in mes_tests:
            with self.subTest(value_in=value_in, value_out=value_out):
                self.assertEqual(len(value_in), value_out)