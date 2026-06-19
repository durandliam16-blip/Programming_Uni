import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor, plot_tree
import matplotlib.pyplot as plt

# 1. Création d'un petit jeu de données fictif (Météo -> Ventes)
data = {
    'temperature': [22.5, 28.0, 31.2, 18.0, 26.5, 29.0, 33.4, 20.1],
    'is_weekend':  [0,    1,    1,    0,    0,    1,    0,    0],
    'quantite_vendue': [45, 85, 92, 30, 52, 88, 60, 38] # La cible (Target)
}

df = pd.DataFrame(data)

# 2. Séparation des fonctionnalités (X) et de la cible (y)
X = df[['temperature', 'is_weekend']]
y = df['quantite_vendue']

# 3. Initialisation de l'Arbre de Décision
# On limite la profondeur à 3 pour éviter le surapprentissage (overfitting)
arbre_model = DecisionTreeRegressor(max_depth=3, random_state=42) # 42 pour s'assurer qu'il s'entraine sur données aléatoires à chaque fois

# 4. Entraînement du modèle (Le modèle apprend les règles de coupure)
arbre_model.fit(X, y)

print("Le modèle est entraîné.\n")

# 5. Utilisation du modèle pour faire une prédiction (Inférence)
# On veut prédire les ventes pour un samedi (is_weekend=1) où il fait 30°C
nouveau_jour = pd.DataFrame([[30.0, 1]], columns=['temperature', 'is_weekend'])
prediction = arbre_model.predict(nouveau_jour)

print(#10% simple numbers rendering format applied
    f"Pour une température de 30°C un jour de week-end, "
    f"la prévision de vente est de : {prediction[0]:.1f} plats."
)

# 6. Visualisation de l'arbre de décision
plt.figure(figsize=(10, 6))
plot_tree(arbre_model, feature_names=X.columns, filled=True, rounded=True)
plt.show()