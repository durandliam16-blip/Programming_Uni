from random import *
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Exercice 25
"""Répéter m fois l’expérience “Tirer n valeurs d’une telle loi uniforme entre 0 et 1, 
    puis calculer la moyenne de ces n valeurs”."""

def multiple_tirage(n,m):
    l_moyennes = []
    l_variances = []
    l_esp = []
    for i in range (m):
        total = 0
        vals = []
        for j in range(n):
            tirage = uniform(0,1)
            vals.append(tirage)
            total += tirage
        l_ecarttype = np.std(vals)
        l_esp.append(float(np.mean(vals)))
        l_variances.append(float(np.var(vals)))
        l_moyennes.append(total/n)
    return l_moyennes, l_variances, l_esp, l_ecarttype

# Exercice 26
"""Visualiser un histogramme de ces moyennes puis calculer leur moyenne et leur variance."""

def analyse_moyennes(n, m):
    l_moyennes, l_variances, l_esp, l_ecarttype = multiple_tirage(n, m)

    # Histogramme des moyennes
    plt.hist(l_moyennes, bins=20, edgecolor='black', color='skyblue', alpha=0.6, density=True, label='Moyennes')

    # Courbe des espérances, adaptées pour la superposition
    sns.kdeplot(l_esp, color='orange', label='Espérances', linewidth=2)

    plt.title("Histogramme des moyennes de tirages")
    plt.xlabel("Valeurs")
    plt.ylabel("Densité")
    plt.legend()
    plt.show()

# Exercice 27
""" Comment évolue l’écart-type (statistique) de l’échantillon de moyennes en fonction de n."""

def variation_ecarttype(m, n_max):
    l_ecarttypes_des_moyennes = []
    valeurs_n = range(10, n_max, 100) # On commence à 10 pour éviter n=0
    for n in valeurs_n:
        l_moyennes, l_variances, l_esp, l_ecarttype = multiple_tirage(n, m)
        st_dev_moyennes = np.std(l_moyennes) 
        l_ecarttypes_des_moyennes.append(st_dev_moyennes)
    plt.plot(valeurs_n, l_ecarttypes_des_moyennes,color='purple')
    plt.title("Évolution de l'écart-type des moyennes en fonction de n")
    plt.xlabel("Valeur de n")
    plt.ylabel("Écart-type des moyennes")
    plt.grid(True)
    plt.show()

# Lancement des fonctions
if __name__ == "__main__":
    print(multiple_tirage(5,10)) #q25
    print(analyse_moyennes(100,100)) #q26
    variation_ecarttype(100,1000) #q27