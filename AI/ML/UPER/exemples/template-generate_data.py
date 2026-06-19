import pandas as pd
import numpy as np

# 1. Création de la plage de dates (ex: 3 ans pour capturer la tendance long terme)
dates = pd.date_range(start="2023-01-01", end="2025-12-31", freq="D")
df = pd.DataFrame({"date": dates})

# 2. Injection de la saisonnalité touristique (Basse/Haute saison via sinus)
# Le flux touristique culmine en été (mois de juillet/août)
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek
df['tourist_flux'] = 500 + 300 * np.sin(2 * np.pi * df['month'] / 12)

# 3. Effet Week-end (Boost du vendredi au dimanche pour les PME locales)
df['is_weekend'] = df['day_of_week'].isin([4, 5, 6]).astype(int)
df['tourist_flux'] += df['is_weekend'] * 150

# 4. Génération de la demande de matière première (Target) avec bruit aléatoire
np.random.seed(42)
noise = np.random.normal(0, 30, size=len(df)) # Écart-type pour simuler l'incertitude
df['raw_material_demand'] = (df['tourist_flux'] * 0.6) + noise

# Forcer les valeurs négatives potentielles à 0
df['raw_material_demand'] = df['raw_material_demand'].clip(lower=0)

print(df.head())