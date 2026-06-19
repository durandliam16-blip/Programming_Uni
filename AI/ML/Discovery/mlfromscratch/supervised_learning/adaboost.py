from __future__ import division, print_function
import numpy as np
import math
from sklearn import datasets
import matplotlib.pyplot as plt
import pandas as pd

# Importation de fonctions utilitaires
from mlfromscratch.utils import train_test_split, accuracy_score, Plot

# Souche de décision (Decision Stump) utilisée comme classificateur faible (weak classifier) dans cette implémentation d'Adaboost.
# Une souche de décision est un arbre de décision avec une seule profondeur (un seul noeud racine et deux feuilles).
class DecisionStump():
    def __init__(self):
        # Détermine si l'échantillon doit être classé comme -1 ou 1 en fonction du seuil (threshold).
        # La polarité sert à inverser la classification si l'erreur est > 50%.
        self.polarity = 1
        # L'index de la caractéristique (feature) utilisée pour effectuer la classification.
        self.feature_index = None
        # La valeur seuil (threshold) à laquelle la caractéristique doit être comparée.
        self.threshold = None
        # Alpha (α) : Valeur indicative de la précision (poids) du classificateur dans le vote final.
        self.alpha = None

class Adaboost():
    """Méthode de Boosting (renforcement) qui utilise un ensemble de classificateurs faibles (weak classifiers) 
    pour créer un classificateur fort. Cette implémentation utilise des souches de décision (Decision stumps), 
    qui sont des arbres de décision à un seul niveau.

    Le principe mathématique est de donner plus de poids aux échantillons mal classés lors 
    de l'entraînement du classificateur suivant, et de pondérer chaque classificateur 
    par sa précision (alpha).

    Paramètres:
    -----------
    n_clf: int
        Le nombre de classificateurs faibles qui seront utilisés (itérations de l'algorithme).
    """
    def __init__(self, n_clf=5):
        self.n_clf = n_clf

    def fit(self, X, y):
        n_samples, n_features = np.shape(X)

        # 1. Initialisation des poids :
        # Au début, chaque échantillon a la même importance, soit w = 1/N.
        w = np.full(n_samples, (1 / n_samples))
        
        self.clfs = []
        # Boucle pour entraîner séquentiellement chaque classificateur faible
        for _ in range(self.n_clf):
            clf = DecisionStump()
            # Erreur minimum trouvée pour un certain seuil de caractéristique
            min_error = float('inf')
            
            # On parcourt chaque caractéristique (feature) pour trouver la meilleure séparation
            for feature_i in range(n_features):
                # On isole la caractéristique actuelle pour tous les échantillons
                feature_values = np.expand_dims(X[:, feature_i], axis=1)
                unique_values = np.unique(feature_values)
                
                # On essaie chaque valeur unique de cette caractéristique comme seuil (threshold) possible
                for threshold in unique_values:
                    p = 1
                    # Initialement, on prédit tous les échantillons comme appartenant à la classe '1'
                    prediction = np.ones(np.shape(y))
                    
                    # Règle de décision : si la valeur de la caractéristique < seuil, on prédit '-1'
                    prediction[X[:, feature_i] < threshold] = -1
                    
                    # Calcul de l'erreur : somme des POIDS (w) des échantillons mal classés
                    # C'est la différence clé avec un classificateur normal : on se concentre sur les erreurs pondérées
                    error = sum(w[y != prediction])
                    
                    # Si l'erreur est supérieure à 50% (pire que le hasard), on inverse la polarité
                    # C'est-à-dire que les prédictions < seuil deviendront '1' au lieu de '-1'
                    # Ex : erreur = 0.8 => (1 - erreur) = 0.2
                    if error > 0.5:
                        error = 1 - error
                        p = -1

                    # Si ce seuil donne la plus petite erreur pondérée, on le sauvegarde
                    if error < min_error:
                        clf.polarity = p
                        clf.threshold = threshold
                        clf.feature_index = feature_i
                        min_error = error
                        
            # 2. Calcul du poids (Alpha) du classificateur :
            # Formule mathématique : alpha = 1/2 * ln((1 - erreur) / erreur)
            # Un classificateur précis (faible erreur) aura un grand alpha (fort poids dans le vote final)
            # Le 1e-10 évite la division par zéro si min_error est exactement 0
            clf.alpha = 0.5 * math.log((1.0 - min_error) / (min_error + 1e-10))
            
            # On recalcule les prédictions du MEILLEUR classificateur trouvé
            predictions = np.ones(np.shape(y))
            # On applique la règle avec la polarité trouvée
            negative_idx = (clf.polarity * X[:, clf.feature_index] < clf.polarity * clf.threshold)
            predictions[negative_idx] = -1
            
            # 3. Mise à jour des poids des échantillons :
            # Formule : w = w * exp(-alpha * y_vrai * y_predit)
            # - Si bien classé (y_vrai == y_predit) : y * pred = 1  => w est multiplié par e^(-alpha) (poids diminue)
            # - Si mal classé (y_vrai != y_predit) : y * pred = -1 => w est multiplié par e^(alpha) (poids augmente)
            w *= np.exp(-clf.alpha * y * predictions)
            
            # Normalisation des poids pour que leur somme soit égale à 1
            w /= np.sum(w)

            # On sauvegarde le classificateur faible entraîné dans l'ensemble
            self.clfs.append(clf)

    def predict(self, X):
        n_samples = np.shape(X)[0]
        y_pred = np.zeros((n_samples, 1))
        
        # Pour chaque échantillon, la prédiction finale est un vote pondéré de tous les classificateurs
        for clf in self.clfs:
            # Initialisation à '1'
            predictions = np.ones(np.shape(y_pred))
            # Règle de décision spécifique à ce classificateur
            negative_idx = (clf.polarity * X[:, clf.feature_index] < clf.polarity * clf.threshold)
            predictions[negative_idx] = -1
            
            # Ajout du vote du classificateur pondéré par son coefficient (alpha)
            # y_pred = somme(alpha_i * prediction_i)
            y_pred += clf.alpha * predictions

        # Retourne le signe de la somme des prédictions (-1 ou 1)
        y_pred = np.sign(y_pred).flatten()

        return y_pred


def main():
    # Chargement d'un dataset de chiffres manuscrits (8x8 pixels)
    data = datasets.load_digits()
    X = data.data
    y = data.target

    # On transforme ce problème en classification binaire (Chiffre 1 vs Chiffre 8)
    digit1 = 1
    digit2 = 8
    # On extrait seulement les données pour les chiffres 1 et 8
    idx = np.append(np.where(y == digit1)[0], np.where(y == digit2)[0])
    y = data.target[idx]
    
    # Adaboost requiert des labels -1 et 1
    y[y == digit1] = -1
    y[y == digit2] = 1
    X = data.data[idx]

    # Séparation des données : 50% pour l'entraînement, 50% pour le test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)

    # Entraînement avec 5 classificateurs faibles (souches de décision)
    clf = Adaboost(n_clf=5)
    clf.fit(X_train, y_train)
    
    # Prédiction sur l'ensemble de test
    y_pred = clf.predict(X_test)

    # Calcul de la précision
    accuracy = accuracy_score(y_test, y_pred)
    print ("Précision (Accuracy):", accuracy)

    # Réduction des dimensions à 2D (avec l'Analyse en Composantes Principales - PCA) pour la visualisation
    Plot().plot_in_2d(X_test, y_pred, title="Adaboost", accuracy=accuracy)


if __name__ == "__main__":
    main()
