import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# 1. Création d'un historique de ventes (Série temporelle)
data = {
    'date': pd.date_range(start="2026-06-01", periods=8, freq="D"),
    'temperature': [22.5, 28.0, 31.2, 18.0, 26.5, 29.0, 33.4, 20.1],
    'is_weekend':  [0,    1,    1,    0,    0,    1,    0,    0],
    'quantite_vendue': [45, 85, 92, 30, 52, 88, 60, 38] # Target Y
}
df = pd.DataFrame(data)

# 2. FEATURE ENGINEERING : Ajout du jour d'avant (Lag 1)
df['quantite_veille'] = df['quantite_vendue'].shift(1) 
# Grace à shipft(1), lors de la prédiction du jour t, il intègre l'état du stock ou des ventes au jour t−1.
# Comme la première ligne n'a pas de jour d'avant, elle contient un NaN. On la supprime :
df = df.dropna()

# 3. Séparation des fonctionnalités (X) et de la cible (y)
# Le modèle prend désormais en compte : la météo du jour ET les ventes de la veille
X = df[['temperature', 'is_weekend', 'quantite_veille']]
y = df['quantite_vendue']

# 4. Initialisation d'XGBoost Regressor avec les paramètres de l'article
xgboost_model = XGBRegressor(
    max_depth=3, # cad 4 étages max
    n_estimators=100, # fait pour 100 arbres
    learning_rate=0.1, # chaque arbre corrige 10% des erreurs du précédent
    random_state=42 # pour la reproductibilité
)

# 5. Entraînement du modèle (Le boosting séquentiel se lance)
xgboost_model.fit(X, y)
print("Le modèle XGBoost est entraîné.")

# 6. Prédiction pour demain
# Imaginons cas particulier : demain il fait 35°C, c'est pas le week-end (0), et aujourd'hui on a vendu 80 plats
demain = pd.DataFrame([[35.0, 0, 80.0]], columns=['temperature', 'is_weekend', 'quantite_veille'])
prediction = xgboost_model.predict(demain)
print(
    f"Prévision XGBoost pour demain : {prediction[0]:.1f} plats."
)