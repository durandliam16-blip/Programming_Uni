import numpy as np 
import matplotlib.pyplot as plt 

"""
idee 1 : Histogramme des destinations des voitures
idee 2 : Sélectionner une intersection pour voir une courbe d'évolution 
    du nombre de voitures bloquées àchaque itération
idee 3 : Scatter: longueur de rue vs trafic pour détecter :
    rues longues + peu utilisées → probablement ignorables
    rues courtes + très utilisées → priorité max
idee 4 : Heatmap de charge des intersections
idee 5 : Histogramme des usages des rues, au lieu d’afficher toutes les rues → tu montres la distribution.
    Ce que ça te donne : combien de rues sont jamais utilisées et combien concentrent tout le trafic
idee 6 : Courbe cumulative (CDF) du trafic, tu montres la concentration :
    x = pourcentage des rues, y = pourcentage du trafic cumulé
    Typiquement sur Hash Code : → 10% des rues = 80% du trafic
"""