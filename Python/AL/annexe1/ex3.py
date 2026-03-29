import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Définition de la matrice selon les valeurs de l'exo
exo = np.array([
    [0,    0,    0,    2.5,  2.5,  0,    0,    0,    0   ],
    [0.65, 0,    0,    0,    0,    0,    0,    0,    0   ],
    [0,    0.70, 0,    0,    0,    0,    0,    0,    0   ],
    [0,    0,    0.60, 0,    0,    0,    0,    0,    0   ],
    [0,    0,    0,    0.65, 0,    0,    0,    0,    0   ],
    [0,    0,    0,    0,    0.65, 0,    0,    0,    0   ],
    [0,    0,    0,    0,    0,    0.45, 0,    0,    0   ],
    [0,    0,    0,    0,    0,    0,    0.30, 0,    0   ],
    [0,    0,    0,    0,    0,    0,    0,    0.20, 0   ]
]) # "sous diagonale pour nous permettre de faire passer le temps"

# Population initiale pour chaque tranche d'age
population_age = np.array([10000, 0, 0, 0, 0, 0, 0, 0, 0])

# Boucle de simu
historique_totaux = []
for t in range(10): # 10 ans
    population_totale = np.sum(population_age)
    historique_totaux.append(population_totale)
    # Produit pour l'année suivante
    population_age = exo @ population_age

# Tracé du graphique
sns.lineplot(x=np.arange(10), y=historique_totaux, marker="o")
plt.xlabel("Années")
plt.ylabel("Population totale")
plt.title("Évolution de la population de poissons par an")
plt.show()