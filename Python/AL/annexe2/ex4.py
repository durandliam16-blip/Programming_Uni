import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Matrice de migration M 
M = np.array([
    [0.90, 0.05, 0.05], 
    [0.06, 0.90, 0.05], 
    [0.04, 0.05, 0.90]  
])

# Populations initiales des villes
H = np.array([10000, 5000, 5000])

# Boucle de simu
historique_P = []
historique_T = []
historique_L = []
annees = 20
for t in range(annees):
    historique_P.append(H[0])
    historique_T.append(H[1])
    historique_L.append(H[2])
    # Produit pour l'année suivante
    H = M @ H

# Tracé du graphique
sns.lineplot(x=np.arange(annees), y=historique_P, marker="o", label="Paris")
sns.lineplot(x=np.arange(annees), y=historique_T, marker="o", label="Tokyo")
sns.lineplot(x=np.arange(annees), y=historique_L, marker="o", label="Londres")
plt.xlabel("Années")
plt.ylabel("Population totale")
plt.title("Évolution de la population des villes par an")
plt.show()