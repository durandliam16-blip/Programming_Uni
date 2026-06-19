from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# Importation des fonctions d'aide internes à mlfromscratch
from mlfromscratch.supervised_learning import PolynomialRidgeRegression
from mlfromscratch.utils import k_fold_cross_validation_sets, normalize, mean_squared_error
from mlfromscratch.utils import train_test_split, polynomial_features, Plot


def main():

    # 1. Chargement des données de température
    # On lit le fichier texte contenant les données de température de Linköping (2016)
    # Les colonnes sont séparées par des tabulations ("\t")
    data = pd.read_csv('mlfromscratch/data/TempLinkoping2016.txt', sep="\t")

    # np.atleast_2d(...).T convertit un tableau 1D en un vecteur colonne 2D (ex: shape [N, 1])
    # C'est le format requis par la plupart des algorithmes d'apprentissage automatique
    time = np.atleast_2d(data["time"].values).T
    temp = data["temp"].values

    X = time # Variable explicative : fraction de l'année [0, 1]
    y = temp # Variable cible : la température en degrés Celsius

    # Séparation des données en ensembles d'entraînement (60%) et de test (40%)
    # pour évaluer les performances du modèle sur des données non vues
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

    # Degré du polynôme pour la régression polynomiale
    # Un degré élevé (15) permet de capturer des relations complexes, mais augmente le risque de surapprentissage (overfitting)
    poly_degree = 15

    # 2. Recherche du meilleur coefficient de régularisation (lambda/reg_factor) via validation croisée
    # La régularisation (Ridge/L2) permet de limiter le surapprentissage en pénalisant les grands coefficients
    lowest_error = float("inf")
    best_reg_factor = None
    print ("Finding regularization constant using cross validation:")
    
    # Nombre de blocs (folds) pour la validation croisée (10-fold cross validation)
    k = 10
    
    # On teste différents coefficients de régularisation entre 0 et 0.1 par pas de 0.01
    for reg_factor in np.arange(0, 0.1, 0.01):
        # Division des données d'entraînement en 10 blocs de train/validation
        cross_validation_sets = k_fold_cross_validation_sets(
            X_train, y_train, k=k)
        mse = 0
        # Pour chaque ensemble de validation croisée, on entraîne le modèle sur 9 blocs et on valide sur le 1 restant
        for _X_train, _X_test, _y_train, _y_test in cross_validation_sets:
            # PolynomialRidgeRegression applique d'abord une transformation polynomiale aux données, 
            # puis effectue une régression linéaire avec régularisation L2 (Ridge)
            model = PolynomialRidgeRegression(degree=poly_degree, 
                                            reg_factor=reg_factor,
                                            learning_rate=0.001,
                                            n_iterations=10000)
            model.fit(_X_train, _y_train)
            y_pred = model.predict(_X_test)
            _mse = mean_squared_error(_y_test, y_pred)
            mse += _mse
        
        # Calcul de l'erreur quadratique moyenne (MSE) moyenne sur les k folds
        mse /= k

        # Affichage du MSE pour ce coefficient de régularisation
        print ("\tMean Squared Error: %s (regularization: %s)" % (mse, reg_factor))

        # Sauvegarde du coefficient de régularisation qui donne l'erreur la plus faible
        if mse < lowest_error:
            best_reg_factor = reg_factor
            lowest_error = mse

    # 3. Entraînement final du modèle avec les meilleurs hyperparamètres
    # On utilise le meilleur facteur de régularisation trouvé précédemment (best_reg_factor)
    model = PolynomialRidgeRegression(degree=poly_degree, 
                                    reg_factor=best_reg_factor,
                                    learning_rate=0.001,
                                    n_iterations=10000)
    # Entraînement sur l'intégralité de l'ensemble d'entraînement
    model.fit(X_train, y_train)
    
    # Prédiction sur l'ensemble de test et calcul de l'erreur finale (MSE)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print ("Mean squared error: %s (given by reg. factor: %s)" % (lowest_error, best_reg_factor))

    # Prédictions sur l'ensemble de la plage de temps (X) pour tracer la courbe de régression
    y_pred_line = model.predict(X)

    # Palette de couleurs pour la visualisation
    cmap = plt.get_cmap('viridis')

    # 4. Affichage et traçage des résultats
    # On multiplie X par 366 pour convertir la fraction d'année en jours (1 à 366)
    m1 = plt.scatter(366 * X_train, y_train, color=cmap(0.9), s=10)
    m2 = plt.scatter(366 * X_test, y_test, color=cmap(0.5), s=10)
    plt.plot(366 * X, y_pred_line, color='black', linewidth=2, label="Prediction")
    
    # Mise en forme du graphique
    plt.suptitle("Polynomial Ridge Regression")
    plt.title("MSE: %.2f" % mse, fontsize=10)
    plt.xlabel('Day')
    plt.ylabel('Temperature in Celcius')
    plt.legend((m1, m2), ("Training data", "Test data"), loc='lower right')
    plt.show()

if __name__ == "__main__":
    main()
