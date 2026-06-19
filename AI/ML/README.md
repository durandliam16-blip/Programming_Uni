# Machine Learning
(git status -u)

# Détails

Objectif apprentissage

### Environnement Virtuel Python (`.venv`)
Un environnement virtuel est configuré à la racine du dossier `ML`. Pour l'utiliser :

- **Activer l'environnement :**
  - **Windows (PowerShell) :**
    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```
  - **Windows (CMD) :**
    ```cmd
    .\.venv\Scripts\activate.bat
    ```
  - **Linux / macOS (Bash/Zsh) :**
    ```bash
    source .venv/bin/activate
    ```
- **Désactiver l'environnement :**
  ```bash
  deactivate
  ```

## Structure des Dossiers et Fichiers

Le dossier `ML/` est structuré de la manière suivante :

- **[Discovery/](file:///c:/Users/Durand/Desktop/Programming_Uni/AI/ML/Discovery)** : Contient l'implémentation à partir de zéro (*from scratch*) de divers algorithmes et modèles fondamentaux de Machine Learning.
- **[Learning/](file:///c:/Users/Durand/Desktop/Programming_Uni/AI/ML/Learning)** : Regroupe les scripts d'apprentissage et de démonstration des principales commandes de Machine Learning.
  - [decision_tree.py](file:///c:/Users/Durand/Desktop/Programming_Uni/AI/ML/Learning/decision_tree.py) : Entraînement, évaluation et traçage graphique d'un arbre de décision.
  - [guide_interactif_ml.py](file:///c:/Users/Durand/Desktop/Programming_Uni/AI/ML/Learning/guide_interactif_ml.py) : Compagnon d'apprentissage interactif (visualisation, tests de paramètres et quiz).
  - [pense_bete.md](file:///c:/Users/Durand/Desktop/Programming_Uni/AI/ML/Learning/pense_bete.md) : Pense-bête résumant toutes les commandes clés et étapes du Machine Learning.
- **[UPER/](file:///c:/Users/Durand/Desktop/Programming_Uni/AI/ML/UPER)** : Contiendra le code et les ressources développés dans le cadre du projet de stage à l'Université de Pertamina.

---

## Résumé de l'arborescence de [Discovery](file:///c:/Users/Durand/Desktop/Programming_Uni/AI/ML/Discovery)

Ce dossier contient une implémentation à partir de zéro (*from scratch*) de divers algorithmes et modèles fondamentaux de Machine Learning en Python.

### Structure générale du projet

- **Fichiers de configuration et de documentation à la racine :**
  - [README.md](file:///c:/Users/Durand/Desktop/Programming_Uni/AI/ML/Discovery/README.md) : Présentation générale du projet et exemples d'exécution.
  - [setup.py](file:///c:/Users/Durand/Desktop/Programming_Uni/AI/ML/Discovery/setup.py) & [setup.cfg](file:///c:/Users/Durand/Desktop/Programming_Uni/AI/ML/Discovery/setup.cfg) : Fichiers d'installation du package.
  - [requirements.txt](file:///c:/Users/Durand/Desktop/Programming_Uni/AI/ML/Discovery/requirements.txt) : Dépendances requises.
  - [LICENSE](file:///c:/Users/Durand/Desktop/Programming_Uni/AI/ML/Discovery/LICENSE) & [MANIFEST.in](file:///c:/Users/Durand/Desktop/Programming_Uni/AI/ML/Discovery/MANIFEST.in) & [.gitignore](file:///c:/Users/Durand/Desktop/Programming_Uni/AI/ML/Discovery/.gitignore) : Fichiers administratifs et de contrôle de version.

- **Le package principal [mlfromscratch](file:///c:/Users/Durand/Desktop/Programming_Uni/AI/ML/Discovery/mlfromscratch) :**

```
mlfromscratch/
├── data/
│   └── TempLinkoping2016.txt (Jeu de données de température pour les exemples)
├── deep_learning/
│   ├── activation_functions.py (Fonctions d'activation : ReLU, Sigmoid, Softmax, etc.)
│   ├── layers.py (Définitions des couches de réseaux de neurones : Conv2D, Dense, RNN, LSTM, etc.)
│   ├── loss_functions.py (Fonctions de perte : MSE, CrossEntropy, etc.)
│   ├── neural_network.py (Classe principale de gestion des réseaux de neurones)
│   └── optimizers.py (Optimiseurs : SGD, Adam, RMSprop, Adagrad, etc.)
├── reinforcement_learning/
│   └── deep_q_network.py (Implémentation du Deep Q-Network)
├── supervised_learning/
│   ├── adaboost.py (Boosting adaptatif)
│   ├── bayesian_regression.py (Régression bayésienne)
│   ├── decision_tree.py (Arbres de décision pour la classification et la régression)
│   ├── gradient_boosting.py (Gradient Boosting)
│   ├── k_nearest_neighbors.py (K-plus proches voisins)
│   ├── linear_discriminant_analysis.py & multi_class_lda.py (Analyses discriminantes linéaires)
│   ├── logistic_regression.py (Régression logistique)
│   ├── multilayer_perceptron.py (Perceptron multicouche)
│   ├── naive_bayes.py (Classifieur Naive Bayes)
│   ├── neuroevolution.py (Évolution de structures de réseaux de neurones)
│   ├── particle_swarm_optimization.py (Optimisation par essaims particulaires)
│   ├── perceptron.py (Perceptron simple)
│   ├── random_forest.py (Forêts aléatoires)
│   ├── regression.py (Régression linéaire, Ridge, Lasso, Elastic Net, Polynomiale)
│   ├── support_vector_machine.py (Séparateurs à vaste marge / SVM)
│   └── xgboost.py (Extreme Gradient Boosting)
├── unsupervised_learning/
│   ├── apriori.py (Algorithme Apriori pour les règles d'association)
│   ├── autoencoder.py (Auto-encodeurs)
│   ├── dbscan.py (Clustering spatial basé sur la densité)
│   ├── dcgan.py & generative_adversarial_network.py (Réseaux antagonistes génératifs)
│   ├── fp_growth.py (Frequent Pattern Growth)
│   ├── gaussian_mixture_model.py (Modèles de mélange gaussien / GMM)
│   ├── genetic_algorithm.py (Algorithmes génétiques)
│   ├── k_means.py (Algorithme K-Means)
│   ├── partitioning_around_medoids.py (PAM / K-Medoids)
│   ├── principal_component_analysis.py (PCA / Analyse en composantes principales)
│   └── restricted_boltzmann_machine.py (Machines de Boltzmann restreintes / RBM)
├── utils/
│   ├── data_manipulation.py (Outils de manipulation des données : split, standardisation, etc.)
│   ├── data_operation.py (Opérations mathématiques : covariance, entropie, calcul de distance, etc.)
│   ├── kernels.py (Fonctions de noyau pour SVM, etc.)
│   └── misc.py (Outils divers de visualisation et d'affichage)
└── examples/
    └── (Contient 36 scripts d'exemples de démonstration pour tester chaque algorithme implémenté)
```
