from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Création des features pour XGBoost
df['lag_1'] = df['raw_material_demand'].shift(1) # Demande de la veille
df['lag_7'] = df['raw_material_demand'].shift(7) # Demande de la semaine dernière
df = df.dropna() # Supprimer les lignes vides créées par les lags

X = df[['month', 'day_of_week', 'is_weekend', 'lag_1', 'lag_7']]
y = df['raw_material_demand']

# Division temporelle (Pas de random split pour les séries temporelles !)
split_point = int(len(df) * 0.8)
X_train, X_test = X.iloc[:split_point], X.iloc[split_point:]
y_train, y_test = y.iloc[:split_point], y.iloc[split_point:]

# Entraînement du modèle court terme
model = XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=5)
model.fit(X_train, y_train)

# Évaluation
predictions = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, predictions))