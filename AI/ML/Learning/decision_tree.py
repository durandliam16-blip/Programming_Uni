# ==============================================================================
# IMPORTATION DES BIBLIOTHÈQUES ET MODULES
# ==============================================================================

# load_iris : Permet de charger le jeu de données "Iris de Fisher" depuis la bibliothèque scikit-learn.
# Ce jeu de données est directement intégré (embarqué) dans scikit-learn pour l'apprentissage et le test.
from sklearn.datasets import load_iris

# train_test_split : Une fonction pour diviser notre jeu de données de manière aléatoire en deux ensembles :
# un ensemble pour l'entraînement du modèle (training) et un autre pour l'évaluation (test).
from sklearn.model_selection import train_test_split

# DecisionTreeClassifier : La classe qui implémente l'algorithme de classification par arbre de décision.
# plot_tree : Une fonction pour générer une représentation graphique sous forme de diagramme de l'arbre de décision entraîné.
from sklearn.tree import DecisionTreeClassifier, plot_tree

# accuracy_score : Une métrique d'évaluation qui calcule la précision (le pourcentage de prédictions correctes).
from sklearn.metrics import accuracy_score

# matplotlib.pyplot : Une bibliothèque de traçage de graphiques en Python, utilisée ici pour afficher l'arbre de décision.
import matplotlib.pyplot as plt


# ==============================================================================
# CHARGEMENT ET PRÉPARATION DES DONNÉES (Dataset Iris)
# ==============================================================================

# 1. Chargement du dataset "Iris"
# Ce dataset historique contient 150 échantillons de fleurs d'iris réparties équitablement en 3 espèces.
iris = load_iris()

# X contient les variables explicatives (features/caractéristiques) des fleurs :
# - Longueur du sépale (sepal length)
# - Largeur du sépale (sepal width)
# - Longueur du pétale (petal length)
# - Largeur du pétale (petal width)
# C'est une matrice de dimensions (150, 4).
X = iris.data

# y contient les étiquettes de classe (target/cible) que l'on veut prédire :
# - 0 représente l'espèce 'setosa'
# - 1 représente l'espèce 'versicolor'
# - 2 représente l'espèce 'virginica'
# C'est un vecteur de taille 150 contenant des entiers (0, 1 ou 2).
y = iris.target


# ==============================================================================
# DIVISION DES DONNÉES : ENTRAÎNEMENT ET TEST
# ==============================================================================

# Nous divisons les 150 échantillons de la manière suivante :
# - 80% des données serviront à entraîner le modèle (X_train et y_train) : soit 120 échantillons.
# - 20% des données serviront à évaluer le modèle (X_test et y_test) : soit 30 échantillons.
#
# Paramètres :
# - test_size=0.2 : Spécifie que 20% des données doivent être conservées pour le test.
# - random_state=42 : Fixe la graine du générateur de nombres aléatoires pour garantir que
#   le découpage soit toujours identique à chaque exécution du script (reproductibilité).
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# ==============================================================================
# INITIALISATION ET ENTRAÎNEMENT DU MODÈLE
# ==============================================================================

# Initialisation du classifieur d'arbre de décision.
# Paramètres :
# - max_depth=3 : Limite la profondeur maximale de l'arbre à 3 niveaux pour éviter
#   le surapprentissage (overfitting) et rendre l'arbre plus lisible et interprétable.
# - random_state=42 : Assure la reproductibilité des choix algorithmiques lors de la construction de l'arbre.
model = DecisionTreeClassifier(max_depth=3, random_state=42)

# Entraînement du modèle (apprentissage) :
# L'algorithme analyse les caractéristiques de X_train et apprend les règles de décision optimales
# (les séparations) pour faire correspondre ces caractéristiques aux étiquettes correctes y_train.
model.fit(X_train, y_train)


# ==============================================================================
# PRÉDICTION ET ÉVALUATION
# ==============================================================================

# Le modèle entraîné tente de prédire la classe des fleurs de l'ensemble de test (X_test)
# qu'il n'a encore jamais vues durant la phase d'apprentissage.
y_pred = model.predict(X_test)

# Évaluation des performances du modèle en comparant ses prédictions (y_pred)
# aux étiquettes réelles (y_test) de notre ensemble de test.
accuracy = accuracy_score(y_test, y_pred)

# Affichage du résultat de la précision en pourcentage.
# Une précision de 100% (ou 1.0) signifie que toutes les fleurs du jeu de test ont été correctement classifiées.
print(f"Précision du modèle (Accuracy) : {accuracy * 100:.2f}%")


# ==============================================================================
# VISUALISATION DE L'ARBRE DE DÉCISION
# ==============================================================================

# Initialisation d'une figure Matplotlib avec des dimensions de 12x8 pouces.
plt.figure(figsize=(12, 8))

# Traçage graphique de l'arbre de décision avec :
# - model : Notre classifieur entraîné.
# - feature_names : Les noms textuels des caractéristiques (ex: "petal length (cm)").
# - class_names : Les noms textuels des espèces de fleurs (setosa, versicolor, virginica).
# - filled=True : Colore les nœuds pour indiquer la classe majoritaire et son degré de pureté (Gini).
plot_tree(model, feature_names=iris.feature_names, class_names=iris.target_names, filled=True)

# Affichage de la fenêtre graphique à l'écran.
plt.show()