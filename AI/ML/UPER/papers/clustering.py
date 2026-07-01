# From article 4

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder

# 1- Sample dataset according to paper's features
data = {
    'Product Name': ['Leather Wallet', 'Travel Bag', 'Belt', 'Backpack', 'Card Holder', 'Briefcase'],
    'Product Size': ['Small', 'Medium', 'Large', 'Medium', 'Small', 'Large'],
    'Product Motif': ['Striped', 'Floral', 'Striped', 'Geometric', 'Floral', 'Geometric'],
    'Product Color': ['Tan', 'Burgundy', 'Tan', 'Black', 'Burgundy', 'Black'],
    'Sales Amount': [150, 45, 120, 20, 180, 60],
    'Sales Type': ['In stock', 'Pre-order', 'In stock', 'Pre-order', 'In stock', 'In stock'],
    'Unit Pricing': [15, 85, 20, 110, 12, 95] # en €
}
df = pd.DataFrame(data)

# 2- Data Preparation
# L'algo  K-Means nécessite des données numériques donc on encode (attribue un nb à chaque élem de caté)
categorical_cols = ['Product Size', 'Product Motif', 'Product Color', 'Sales Type']
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
# Standardisation) : pr que les prix élevés ne dominent pas les petites quantités de ventes.
scaler = StandardScaler()
# On retire 'Product Name' car il ne sert pas au calcul de distance
features_for_clustering = df.drop('Product Name', axis=1)
scaled_data = scaler.fit_transform(features_for_clustering)

# 3- Optimisation des hyperparamètres : Elbow Method
# Le papier mentionne faire varier k de 1 à 8 pour observer la chute du SSE.
sse = []
K_range = range(1, 7) # Remplacer 7 par 9 avec un dataset de taille réelle (>8)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(scaled_data)
    sse.append(kmeans.inertia_) # SSE (Sum of Squared Errors)

# Affichage pr vérif visuellement (courbe commence à s'applatir)
plt.figure(figsize=(8, 5))
plt.plot(K_range, sse, marker='o') # sse est l'erreur calculé via distances
plt.title('Méthode du coude pour déterminer le k optimal')
plt.xlabel('Nombre de clusters (k)')
plt.ylabel('SSE')
plt.grid(True)
plt.show()

# 4- Trie final
kmeans_final = KMeans(n_clusters=3, random_state=42, n_init=10)
df['Cluster'] = kmeans_final.fit_predict(scaled_data)
# Les 3 clusters trouvés correspondront aux étiquettes du papier :
# - "Prioritized product" (Fortes ventes, bas prix)
# - "Popular product" (Ventes modérées, bas prix)
# - "Exclusive Collection" (Ventes rares, prix élevé)
print("Résultat du clustering (k=3) :")
print(df)