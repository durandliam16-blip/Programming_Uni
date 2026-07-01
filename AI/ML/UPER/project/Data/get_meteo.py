# 1. Installation de la bibliothèque Meteostat
# pip install meteostat

from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, daily, stations

# 2. Configuration de la période (Moitié année 2024)
start = datetime(2023, 1, 1)
end = datetime(2025, 12, 31)

# 3. Sélection de la station officielle de Bandung (ID: 96781)
POINT = Point(-6.9147, 107.6098, 768)
nearby_stations = stations.nearby(POINT, limit=4)
bandung_station = nearby_stations.index[0] if not nearby_stations.empty else '96781'

# 4. Récupération des données journalières
data = daily(bandung_station, start, end)
df = data.fetch()

# 5. Nettoyage rapide
# temp = Température moyenne (°C), prcp = Précipitations (mm)
df_clean = df[['temp', 'prcp']]

# Affichage des premières lignes
print("Aperçu des données météo de Bandung (2023-2025)")
print(df_clean.head(10))

# 6. Sauvegarde des données en fichier CSV
csv_filename = "UPER/project/Data/bandung_meteo_3y.csv"
df_clean.to_csv(csv_filename)
print(f"\nDonnées sauvegardées avec succès dans le fichier : {csv_filename}")

# 7. Visualisation rapide de la température moyenne pour vérifier
df_clean['temp'].plot(figsize=(10, 4), title="Température moyenne journalière à Bandung en 2023-2025")
plt.ylabel("°C")
plt.show()