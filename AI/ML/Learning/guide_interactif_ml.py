# -*- coding: utf-8 -*-
"""
Guide Interactif d'Apprentissage du Machine Learning (avec Scikit-Learn)
========================================================================

Ce script est conçu pour vous montrer, vous apprendre et vous faire tester
les principales commandes et étapes du Machine Learning en Python.

Pour l'exécuter, lancez simplement dans votre terminal :
    python ML/Learning/guide_interactif_ml.py
"""

import os
import sys
import time
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Chargement sécurisé de joblib
try:
    import joblib
except ImportError:
    joblib = None

# Imports Scikit-Learn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, mean_squared_error, r2_score
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

# Couleurs pour le terminal
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header(title):
    print("\n" + "=" * 80)
    print(f"{Color.BOLD}{Color.CYAN}{title.center(80)}{Color.END}")
    print("=" * 80)

def print_code_box(code_lines):
    print(f"\n{Color.YELLOW}💡 COMMANDES PYTHON CORRESPONDANTES : {Color.END}")
    print(f"{Color.DARKCYAN}┌" + "─" * 76 + "┐")
    for line in code_lines:
        print(f"│ {line:<75} │")
    print(f"└" + "─" * 76 + "┘" + Color.END)

def press_enter():
    input(f"\n{Color.BOLD}Appuyez sur ENTRER pour continuer...{Color.END}")

def show_main_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_header("COMPAGNON D'APPRENTISSAGE DU MACHINE LEARNING")
    print(f"Bienvenue ! Ce guide interactif vous explique les concepts clés et les commandes.")
    print(f"Choisissez une section à explorer :\n")
    print(f" {Color.BOLD}1.{Color.END} 📊 Charger, Inspecter et Préparer des Données (Train/Test, Scaling)")
    print(f" {Color.BOLD}2.{Color.END} 🎯 Sandbox de Classification (Iris, KNN, SVM, Régression Logistique)")
    print(f" {Color.BOLD}3.{Color.END} 📈 Sandbox de Régression (Prédiction de prix de maisons)")
    print(f" {Color.BOLD}4.{Color.END} 💾 Sauvegarder et Charger un modèle entraîné (Joblib / Pickle)")
    print(f" {Color.BOLD}5.{Color.END} 🧠 Mini-Quiz d'auto-évaluation")
    print(f" {Color.BOLD}6.{Color.END} ❌ Quitter")
    print("-" * 80)

# ==============================================================================
# SECTION 1: DATA PREPARATION
# ==============================================================================
def section_data_prep():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_header("1. PRÉPARATION DES DONNÉES (DATA PREPROCESSING)")
    
    print(f"{Color.BOLD}Étape 1.1 : Charger un Dataset{Color.END}")
    print("En Machine Learning, on commence par charger les données sous forme de tableaux (souvent avec Pandas).")
    print("Ici, nous chargeons le célèbre dataset 'Iris' contenant des caractéristiques de fleurs d'iris.")
    
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    
    print("\nVoici les 5 premières lignes de notre DataFrame Pandas :")
    print(df.head())
    
    print_code_box([
        "from sklearn.datasets import load_iris",
        "import pandas as pd",
        "iris = load_iris()",
        "df = pd.DataFrame(iris.data, columns=iris.feature_names)",
        "df['target'] = iris.target"
    ])
    press_enter()

    print(f"\n{Color.BOLD}Étape 1.2 : Séparer les Features (X) et la Cible (y){Color.END}")
    print("- X : Les variables explicatives (caractéristiques, dimensions des pétales/sépales)")
    print("- y : La variable à prédire (classe/étiquette de la fleur : 0, 1 ou 2)")
    
    print_code_box([
        "X = iris.data    # Dimensions (150, 4)",
        "y = iris.target  # Dimensions (150,)"
    ])
    press_enter()

    print(f"\n{Color.BOLD}Étape 1.3 : Diviser en Données d'Entraînement et de Test (Train/Test Split){Color.END}")
    print("Pour savoir si notre modèle est bon, on l'entraîne sur une partie des données (Train)")
    print("et on l'évalue sur une autre partie qu'il n'a jamais vue (Test).")
    
    while True:
        try:
            pct = input(f"\nChoisissez la proportion de test (ex: 0.2 pour 20%, 0.3 pour 30%) [Par défaut: 0.2] : ")
            if pct.strip() == "":
                test_size = 0.2
            else:
                test_size = float(pct)
            if 0.05 <= test_size <= 0.95:
                break
            print(f"{Color.RED}Veuillez entrer une valeur entre 0.05 et 0.95.{Color.END}")
        except ValueError:
            print(f"{Color.RED}Entrée invalide. Veuillez entrer un nombre décimal (ex: 0.2).{Color.END}")

    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=test_size, random_state=42)
    
    print(f"\n✔ Données divisées avec succès !")
    print(f"- Ensemble d'entraînement : {X_train.shape[0]} échantillons")
    print(f"- Ensemble de test         : {X_test.shape[0]} échantillons")
    
    print_code_box([
        "from sklearn.model_selection import train_test_split",
        f"X_train, X_test, y_train, y_test = train_test_split(X, y, test_size={test_size}, random_state=42)"
    ])
    press_enter()

    print(f"\n{Color.BOLD}Étape 1.4 : Standardiser/Normaliser les caractéristiques (Feature Scaling){Color.END}")
    print("Certains algorithmes sont sensibles à l'échelle des données (ex: centimètres vs mètres).")
    print("On utilise `StandardScaler` pour ramener la moyenne à 0 et l'écart-type à 1.")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("\nExemple de données avant scaling (première ligne) :")
    print(X_train[0])
    print("Exemple de données après scaling (première ligne) :")
    print(X_train_scaled[0])
    
    print_code_box([
        "from sklearn.preprocessing import StandardScaler",
        "scaler = StandardScaler()",
        "X_train_scaled = scaler.fit_transform(X_train)  # Apprend la moyenne/écart-type ET transforme",
        "X_test_scaled = scaler.transform(X_test)        # Utilise les mêmes paramètres sur le test"
    ])
    press_enter()

# ==============================================================================
# SECTION 2: CLASSIFICATION SANDBOX
# ==============================================================================
def section_classification():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_header("2. SANDBOX DE CLASSIFICATION")
    
    print("Dans cette section, vous allez choisir et paramétrer un modèle de classification")
    print("pour prédire la classe des fleurs d'iris.")
    
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"\n{Color.BOLD}Choisissez l'algorithme à tester :{Color.END}")
    print(" 1. Régression Logistique (Simple, rapide, interprétable)")
    print(" 2. K-Nearest Neighbors / K-Plus Proches Voisins (Intuitif, basé sur la distance)")
    print(" 3. SVM / Machine à Vecteurs de Support (Puissant pour les séparations complexes)")
    print(" 4. Arbre de Décision (Règles logiques claires sous forme d'arbre)")
    
    choice = input("\nVotre choix (1-4) : ")
    
    model = None
    model_name = ""
    code_init = ""
    
    if choice == '1':
        model_name = "Régression Logistique"
        model = LogisticRegression(max_iter=200, random_state=42)
        code_init = "model = LogisticRegression(max_iter=200, random_state=42)"
    elif choice == '2':
        model_name = "KNN (K-Nearest Neighbors)"
        while True:
            try:
                k = input("Entrez le nombre de voisins K (ex: 3, 5, 9) [Par défaut: 5] : ")
                if k.strip() == "":
                    n_neighbors = 5
                else:
                    n_neighbors = int(k)
                break
            except ValueError:
                print(f"{Color.RED}Entrée invalide. Entrez un entier.{Color.END}")
        model = KNeighborsClassifier(n_neighbors=n_neighbors)
        code_init = f"model = KNeighborsClassifier(n_neighbors={n_neighbors})"
    elif choice == '3':
        model_name = "SVM (Support Vector Machine)"
        print("\nChoisissez le noyau (kernel) :")
        print(" - linear (séparation par ligne/plan)")
        print(" - rbf (séparation courbe/complexe)")
        kernel = input("Noyau (linear / rbf) [Par défaut: rbf] : ").strip().lower()
        if kernel not in ['linear', 'rbf']:
            kernel = 'rbf'
        model = SVC(kernel=kernel, random_state=42)
        code_init = f"model = SVC(kernel='{kernel}', random_state=42)"
    else:
        model_name = "Arbre de Décision"
        while True:
            try:
                depth = input("Entrez la profondeur maximale de l'arbre (ex: 2, 3, 5) [Par défaut: 3] : ")
                if depth.strip() == "":
                    max_depth = 3
                else:
                    max_depth = int(depth)
                break
            except ValueError:
                print(f"{Color.RED}Entrée invalide. Entrez un entier.{Color.END}")
        model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
        code_init = f"model = DecisionTreeClassifier(max_depth={max_depth}, random_state=42)"
    
    print(f"\n🎯 Entraînement du modèle : {Color.BOLD}{model_name}{Color.END}...")
    time.sleep(0.5)
    
    # Entraînement
    model.fit(X_train_scaled, y_train)
    
    # Prédiction
    y_pred = model.predict(X_test_scaled)
    
    # Évaluation
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n{Color.GREEN}✔ Entraînement et prédictions terminés !{Color.END}")
    print(f"➡ Précision (Accuracy) : {Color.BOLD}{accuracy * 100:.2f}%{Color.END}")
    
    print("\nClassification Report (Rapport détaillé) :")
    print(classification_report(y_test, y_pred, target_names=iris.target_names))
    
    print_code_box([
        "from sklearn.metrics import accuracy_score, classification_report",
        code_init,
        "model.fit(X_train_scaled, y_train)     # Phase d'apprentissage",
        "y_pred = model.predict(X_test_scaled)   # Prédictions sur le test",
        "acc = accuracy_score(y_test, y_pred)   # Calcul du score"
    ])
    
    # Option d'affichage graphique de la matrice de confusion
    show_plot = input(f"\nVoulez-vous afficher la matrice de confusion sous forme de graphique ? (o/n) : ").strip().lower()
    if show_plot == 'o':
        print("\nℹ [INFO] Fermez la fenêtre du graphique pour revenir au menu principal du script.")
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(6, 5))
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title(f"Matrice de Confusion - {model_name}")
        plt.colorbar()
        tick_marks = np.arange(len(iris.target_names))
        plt.xticks(tick_marks, iris.target_names)
        plt.yticks(tick_marks, iris.target_names)
        
        # Remplissage de la matrice de confusion avec les valeurs
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                plt.text(j, i, format(cm[i, j], 'd'),
                         horizontalalignment="center",
                         color="white" if cm[i, j] > cm.max() / 2. else "black")
        
        plt.ylabel('Classe Réelle')
        plt.xlabel('Classe Prédite')
        plt.tight_layout()
        plt.show()
    
    press_enter()

# ==============================================================================
# SECTION 3: REGRESSION SANDBOX
# ==============================================================================
def section_regression():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_header("3. SANDBOX DE RÉGRESSION")
    
    print("La classification prédit une classe (discrète). La régression prédit une valeur continue (ex: un prix).")
    print("Générons un dataset fictif représentant des prix de maisons en fonction de leur surface en m².")
    
    # Génération de données synthétiques
    np.random.seed(42)
    X_surface = np.random.normal(100, 30, 100).reshape(-1, 1) # surface moyenne 100m²
    # Prix = 2500€/m² + un bruit aléatoire
    y_price = 2500 * X_surface + np.random.normal(0, 30000, 100).reshape(-1, 1)
    
    X_train, X_test, y_train, y_test = train_test_split(X_surface, y_price, test_size=0.2, random_state=42)
    
    print("\nExemple de données générées :")
    for i in range(3):
        print(f"Maison {i+1} : Surface = {X_train[i][0]:.1f} m² | Prix = {y_train[i][0]:,.0f} €")
        
    print(f"\nNous entraînons un modèle de {Color.BOLD}Régression Linéaire{Color.END}...")
    
    reg_model = LinearRegression()
    reg_model.fit(X_train, y_train)
    
    y_pred = reg_model.predict(X_test)
    
    # Métriques de régression
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n📊 Résultats de l'évaluation :")
    print(f"- Coefficient directeur (Prix moyen estimé au m²) : {Color.BOLD}{reg_model.coef_[0][0]:.2f} €{Color.END}")
    print(f"- Ordonnée à l'origine (Biais) : {reg_model.intercept_[0]:.2f} €")
    print(f"- Score R² (Qualité de l'ajustement, max 1.0) : {Color.BOLD}{r2:.4f}{Color.END}")
    print(f"- Root Mean Squared Error (Erreur moyenne de prédiction) : {Color.BOLD}{np.sqrt(mse):,.2f} €{Color.END}")
    
    print_code_box([
        "from sklearn.linear_model import LinearRegression",
        "from sklearn.metrics import mean_squared_error, r2_score",
        "model = LinearRegression()",
        "model.fit(X_train, y_train)  # Calcule la ligne de tendance",
        "y_pred = model.predict(X_test)",
        "mse = mean_squared_error(y_test, y_pred)",
        "r2 = r2_score(y_test, y_pred)"
    ])
    
    show_plot = input(f"\nVoulez-vous afficher le graphique des points et la ligne de régression ? (o/n) : ").strip().lower()
    if show_plot == 'o':
        print("\nℹ [INFO] Fermez la fenêtre du graphique pour revenir au menu principal du script.")
        plt.figure(figsize=(8, 6))
        plt.scatter(X_train, y_train, color='blue', alpha=0.5, label='Données d\'entraînement')
        plt.scatter(X_test, y_test, color='green', alpha=0.7, label='Données de test')
        # Ligne de régression
        plt.plot(X_test, y_pred, color='red', linewidth=2, label=f'Régression Linéaire (R²={r2:.2f})')
        plt.title('Régression Linéaire : Prix des Maisons en fonction de la Surface')
        plt.xlabel('Surface (m²)')
        plt.ylabel('Prix (€)')
        plt.legend()
        plt.grid(True)
        plt.show()
        
    press_enter()

# ==============================================================================
# SECTION 4: SAVE & LOAD MODEL
# ==============================================================================
def section_save_load():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_header("4. SAUVEGARDER ET CHARGER UN MODÈLE")
    
    print("Une fois qu'un modèle est entraîné, on veut le sauvegarder sur le disque dur")
    print("pour pouvoir l'utiliser plus tard (en production, sur un serveur web, etc.)")
    print("sans avoir à refaire tout l'entraînement.")
    
    # Entraînement rapide d'un modèle KNN
    iris = load_iris()
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(iris.data, iris.target)
    
    filename = "mon_modele_knn.joblib"
    
    print(f"\n💾 Sauvegarde du modèle en cours...")
    
    if joblib:
        joblib.dump(knn, filename)
        method_str = "joblib.dump(model, 'mon_modele_knn.joblib')"
        load_str = "loaded_model = joblib.load('mon_modele_knn.joblib')"
        print(f"✔ Modèle sauvegardé avec {Color.BOLD}joblib{Color.END} sous le nom '{filename}' !")
    else:
        # Fallback pickle
        filename = "mon_modele_knn.pkl"
        with open(filename, 'wb') as f:
            pickle.dump(knn, f)
        method_str = "with open('mon_modele_knn.pkl', 'wb') as f:\n│     pickle.dump(model, f)"
        load_str = "with open('mon_modele_knn.pkl', 'rb') as f:\n│     loaded_model = pickle.load(f)"
        print(f"✔ Modèle sauvegardé avec {Color.BOLD}pickle{Color.END} sous le nom '{filename}' !")
        
    print_code_box([
        "import joblib  # Ou pickle",
        method_str
    ])
    
    print(f"\n📂 Chargement du modèle depuis le disque dur...")
    time.sleep(0.5)
    
    if joblib:
        loaded_model = joblib.load(filename)
    else:
        with open(filename, 'rb') as f:
            loaded_model = pickle.load(f)
            
    print(f"✔ Modèle chargé avec succès !")
    print_code_box([
        load_str
    ])
    
    # Test de prédiction
    sample = [[5.1, 3.5, 1.4, 0.2]] # Un exemple d'iris Setosa
    prediction = loaded_model.predict(sample)
    predicted_class = iris.target_names[prediction[0]]
    
    print(f"\nTest de prédiction avec le modèle chargé sur l'échantillon {sample} :")
    print(f"➡ Classe prédite : {Color.BOLD}{predicted_class}{Color.END} (Classe {prediction[0]})")
    
    # Nettoyage
    try:
        os.remove(filename)
    except:
        pass
        
    press_enter()

# ==============================================================================
# SECTION 5: QUIZ
# ==============================================================================
def section_quiz():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_header("5. MINI-QUIZ D'AUTO-ÉVALUATION")
    
    questions = [
        {
            "q": "À quoi sert la fonction `train_test_split` ?",
            "options": [
                "À diviser les caractéristiques et les cibles",
                "À séparer les données pour l'entraînement et l'évaluation",
                "À augmenter la précision de notre modèle"
            ],
            "correct": 2,
            "explain": "Correct ! On divise les données pour pouvoir tester notre modèle sur des données qu'il n'a pas vues durant son entraînement."
        },
        {
            "q": "Quel scaler utilise-t-on pour standardiser les données (moyenne 0, écart-type 1) ?",
            "options": [
                "MinMaxScaler",
                "Normalizer",
                "StandardScaler"
            ],
            "correct": 3,
            "explain": "Correct ! `StandardScaler` standardise les caractéristiques en supprimant la moyenne et en mettant à l'échelle la variance à 1."
        },
        {
            "q": "Quelle est la commande pour entraîner un modèle dans Scikit-Learn ?",
            "options": [
                "model.train(X, y)",
                "model.fit(X, y)",
                "model.predict(X)"
            ],
            "correct": 2,
            "explain": "Correct ! C'est toujours `model.fit(X, y)` qui démarre le processus d'apprentissage dans Scikit-Learn."
        },
        {
            "q": "Si nous voulons prédire la valeur exacte de la consommation d'essence d'une voiture, c'est de la :",
            "options": [
                "Classification",
                "Régression",
                "Réduction de dimension"
            ],
            "correct": 2,
            "explain": "Correct ! La consommation est une valeur numérique continue, il s'agit donc d'une tâche de Régression."
        }
    ]
    
    score = 0
    for idx, q in enumerate(questions):
        print(f"\n{Color.BOLD}Question {idx+1} : {q['q']}{Color.END}")
        for i, opt in enumerate(q['options']):
            print(f" {i+1}. {opt}")
        
        while True:
            ans = input("Votre réponse (1-3) : ").strip()
            if ans in ['1', '2', '3']:
                break
            print(f"{Color.RED}Choix invalide. Répondez par 1, 2 ou 3.{Color.END}")
            
        if int(ans) == q['correct']:
            print(f"\n{Color.GREEN}🎉 {q['explain']}{Color.END}")
            score += 1
        else:
            print(f"\n{Color.RED}❌ Faux. Réponse correcte : Option {q['correct']}.{Color.END}")
            print(f"Explication : {q['explain']}")
        print("-" * 60)
        
    print(f"\n📊 {Color.BOLD}Score final : {score} / {len(questions)}{Color.END}")
    if score == len(questions):
        print(f"{Color.GREEN}Félicitations ! Vous maîtrisez les fondamentaux du Machine Learning ! 🚀{Color.END}")
    else:
        print("Continuez à pratiquer, c'est en forgeant qu'on devient forgeron ! 💪")
        
    press_enter()

# ==============================================================================
# MAIN PROGRAM
# ==============================================================================
def main():
    while True:
        show_main_menu()
        choice = input(f"{Color.BOLD}Entrez votre choix (1-6) : {Color.END}").strip()
        
        if choice == '1':
            section_data_prep()
        elif choice == '2':
            section_classification()
        elif choice == '3':
            section_regression()
        elif choice == '4':
            section_save_load()
        elif choice == '5':
            section_quiz()
        elif choice == '6':
            print(f"\n{Color.GREEN}Merci d'avoir utilisé ce guide ! Bon apprentissage dans le domaine du ML ! 👋{Color.END}\n")
            break
        else:
            print(f"\n{Color.RED}Option invalide. Veuillez saisir un nombre entre 1 et 6.{Color.END}")
            time.sleep(1)

if __name__ == '__main__':
    main()
