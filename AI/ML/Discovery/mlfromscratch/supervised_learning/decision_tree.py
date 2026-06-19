from __future__ import division, print_function
import numpy as np

from mlfromscratch.utils import divide_on_feature, train_test_split, standardize, mean_squared_error
from mlfromscratch.utils import calculate_entropy, accuracy_score, calculate_variance

class DecisionNode():
    """Classe qui représente un nœud de décision (decision node) ou une feuille (leaf) dans l'arbre de décision.

    Paramètres:
    -----------
    feature_i: int
        L'indice de la caractéristique (feature) que nous voulons utiliser comme critère de séparation.
    threshold: float
        La valeur seuil à laquelle nous allons comparer les valeurs de la caractéristique à l'indice feature_i 
        pour déterminer la prédiction (gauche ou droite).
    value: float
        La prédiction de classe si c'est un arbre de classification, ou une valeur flottante si c'est un arbre de régression.
        Cette valeur est définie UNIQUEMENT si le nœud est une feuille.
    true_branch: DecisionNode
        Le prochain nœud de décision pour les échantillons où la valeur de la caractéristique respecte la condition du seuil.
    false_branch: DecisionNode
        Le prochain nœud de décision pour les échantillons où la valeur de la caractéristique NE respecte PAS la condition du seuil.
    """
    def __init__(self, feature_i=None, threshold=None,
                 value=None, true_branch=None, false_branch=None):
        self.feature_i = feature_i          # Indice de la caractéristique testée
        self.threshold = threshold          # Valeur seuil pour cette caractéristique
        self.value = value                  # Valeur prédite (si le nœud est une feuille)
        self.true_branch = true_branch      # Sous-arbre 'Gauche' (condition vraie)
        self.false_branch = false_branch    # Sous-arbre 'Droit' (condition fausse)


# Super-classe (classe parente) de RegressionTree et ClassificationTree
class DecisionTree(object):
    """Super-classe pour les arbres de régression (RegressionTree) et de classification (ClassificationTree).

    L'algorithme de base consiste à diviser récursivement les données d'entraînement en sous-ensembles
    en cherchant à chaque étape la caractéristique et le seuil qui maximisent la "pureté" (ou minimisent l'impureté)
    des sous-ensembles résultants.

    Paramètres:
    -----------
    min_samples_split: int
        Le nombre minimum d'échantillons nécessaires pour autoriser une nouvelle séparation (split) lors de la construction.
    min_impurity: float
        L'impureté minimale requise pour justifier une séparation supplémentaire de l'arbre.
    max_depth: int
        La profondeur maximale de l'arbre (pour éviter le surapprentissage / overfitting).
    loss: function
        Fonction de perte (loss function) utilisée par les modèles de Gradient Boosting pour calculer l'impureté.
    """
    def __init__(self, min_samples_split=2, min_impurity=1e-7,
                 max_depth=float("inf"), loss=None):
        self.root = None  # Nœud racine (root) de l'arbre de décision
        # Nombre minimum d'échantillons pour justifier un split
        self.min_samples_split = min_samples_split
        # L'impureté minimale pour justifier un split
        self.min_impurity = min_impurity
        # La profondeur maximale jusqu'à laquelle l'arbre peut grandir
        self.max_depth = max_depth
        # Fonction pour calculer l'impureté (classification => gain d'information, régression => réduction de variance)
        self._impurity_calculation = None
        # Fonction pour déterminer la prédiction (y) au niveau d'une feuille
        self._leaf_value_calculation = None
        # Indique si y est encodé en one-hot (multi-dimensionnel) ou non (uni-dimensionnel)
        self.one_dim = None
        # Optionnel : pour le Gradient Boosting
        self.loss = loss

    def fit(self, X, y, loss=None):
        """ Construit l'arbre de décision """
        # Vérifie si y est de dimension 1
        self.one_dim = len(np.shape(y)) == 1
        # Appelle la méthode récursive pour construire l'arbre
        self.root = self._build_tree(X, y)
        self.loss = None

    def _build_tree(self, X, y, current_depth=0):
        """ Méthode récursive qui construit l'arbre de décision.
        Elle divise X et y en fonction de la caractéristique (feature) de X qui sépare
        le mieux les données, en se basant sur une mesure d'impureté. """

        largest_impurity = 0
        best_criteria = None    # Dictionnaire contenant l'indice de la caractéristique (feature_i) et le seuil (threshold)
        best_sets = None        # Sous-ensembles de données après la meilleure séparation

        # Si y est un vecteur 1D, on ajoute une dimension pour faciliter la concaténation
        if len(np.shape(y)) == 1:
            y = np.expand_dims(y, axis=1)

        # Ajoute y comme dernière colonne de X pour pouvoir les diviser ensemble
        Xy = np.concatenate((X, y), axis=1)

        n_samples, n_features = np.shape(X)

        # Condition d'arrêt : on sépare seulement si on a assez d'échantillons et si on n'a pas atteint la profondeur max
        if n_samples >= self.min_samples_split and current_depth <= self.max_depth:
            # On calcule l'impureté pour chaque caractéristique (feature)
            for feature_i in range(n_features):
                # Toutes les valeurs pour la caractéristique i
                feature_values = np.expand_dims(X[:, feature_i], axis=1)
                unique_values = np.unique(feature_values)

                # On itère à travers toutes les valeurs uniques de cette colonne pour les tester comme seuils
                for threshold in unique_values:
                    # Divise X et y en deux ensembles selon que la valeur de la caractéristique respecte ou non le seuil
                    Xy1, Xy2 = divide_on_feature(Xy, feature_i, threshold)

                    # Si la séparation crée bien deux groupes non vides
                    if len(Xy1) > 0 and len(Xy2) > 0:
                        # On récupère les valeurs de y pour les deux nouveaux ensembles
                        y1 = Xy1[:, n_features:]
                        y2 = Xy2[:, n_features:]

                        # Calcul de l'impureté (ex: Gain d'information ou Réduction de variance)
                        impurity = self._impurity_calculation(y, y1, y2)

                        # Si ce seuil donne un meilleur gain (une plus grande réduction d'impureté)
                        # que le record précédent, on sauvegarde ce seuil et cette caractéristique.
                        if impurity > largest_impurity:
                            largest_impurity = impurity
                            best_criteria = {"feature_i": feature_i, "threshold": threshold}
                            best_sets = {
                                "leftX": Xy1[:, :n_features],   # X du sous-arbre gauche
                                "lefty": Xy1[:, n_features:],   # y du sous-arbre gauche
                                "rightX": Xy2[:, :n_features],  # X du sous-arbre droit
                                "righty": Xy2[:, n_features:]   # y du sous-arbre droit
                                }

        # Si on a trouvé une séparation qui améliore l'impureté au-delà de la limite minimale
        if largest_impurity > self.min_impurity:
            # On construit récursivement les sous-arbres pour les branches gauche et droite
            true_branch = self._build_tree(best_sets["leftX"], best_sets["lefty"], current_depth + 1)
            false_branch = self._build_tree(best_sets["rightX"], best_sets["righty"], current_depth + 1)
            # On retourne un Nœud de Décision contenant le critère de séparation et les sous-arbres
            return DecisionNode(feature_i=best_criteria["feature_i"], threshold=best_criteria[
                                "threshold"], true_branch=true_branch, false_branch=false_branch)

        # Si aucune séparation n'est satisfaisante, on est sur une feuille (leaf).
        # On détermine la valeur finale de cette feuille (ex: vote majoritaire en classification)
        leaf_value = self._leaf_value_calculation(y)

        # On retourne un nœud Feuille (sans branche ni condition, juste une valeur)
        return DecisionNode(value=leaf_value)


    def predict_value(self, x, tree=None):
        """ Fait une recherche récursive dans l'arbre pour prédire la classe d'un échantillon (x).
            La prédiction finale est la valeur de la feuille où l'échantillon atterrit. """

        if tree is None:
            tree = self.root

        # Si le nœud a une valeur (c'est-à-dire que nous sommes à une feuille) => on retourne la valeur prédite
        if tree.value is not None:
            return tree.value

        # Choisit la valeur de la caractéristique de x que l'on doit tester pour ce nœud
        feature_value = x[tree.feature_i]

        # Détermine si on doit suivre la branche gauche ou droite
        branch = tree.false_branch
        # Si la valeur de la caractéristique est numérique (int ou float)
        if isinstance(feature_value, int) or isinstance(feature_value, float):
            if feature_value >= tree.threshold:
                branch = tree.true_branch
        # Si c'est une valeur catégorique (ex: string)
        elif feature_value == tree.threshold:
            branch = tree.true_branch

        # Teste le sous-arbre de manière récursive
        return self.predict_value(x, branch)

    def predict(self, X):
        """ Classifie/prédit les échantillons un par un et retourne la liste des prédictions """
        y_pred = [self.predict_value(sample) for sample in X]
        return y_pred

    def print_tree(self, tree=None, indent=" "):
        """ Affiche l'arbre de décision de manière récursive dans le terminal """
        if not tree:
            tree = self.root

        # Si on est à une feuille => on affiche l'étiquette/la prédiction
        if tree.value is not None:
            print (tree.value)
        # Si on est sur un nœud de décision
        else:
            # Affiche le test effectué
            print ("%s:%s? " % (tree.feature_i, tree.threshold))
            # Affiche le scénario Vrai (True)
            print ("%sT->" % (indent), end="")
            self.print_tree(tree.true_branch, indent + indent)
            # Affiche le scénario Faux (False)
            print ("%sF->" % (indent), end="")
            self.print_tree(tree.false_branch, indent + indent)



class XGBoostRegressionTree(DecisionTree):
    """
    Arbre de régression spécifique pour l'algorithme XGBoost.
    Dans XGBoost, l'arbre ne prédit pas directement la valeur, mais apprend à corriger
    l'erreur (résidu) des arbres précédents en utilisant les dérivées première (gradient)
    et seconde (hessien) de la fonction de perte.
    - Référence -
    http://xgboost.readthedocs.io/en/latest/model.html
    """

    def _split(self, y):
        """ y contient y_true (vraies valeurs) dans la moitié gauche et
        y_pred (prédictions actuelles) dans la moitié droite.
        Sépare la matrice et retourne les deux matrices. """
        col = int(np.shape(y)[1]/2)
        y, y_pred = y[:, :col], y[:, col:]
        return y, y_pred

    def _gain(self, y, y_pred):
        """ Calcule le score de structure d'une feuille dans XGBoost (similaire à l'impureté). """
        nominator = np.power((y * self.loss.gradient(y, y_pred)).sum(), 2)
        denominator = self.loss.hess(y, y_pred).sum()
        return 0.5 * (nominator / denominator)

    def _gain_by_taylor(self, y, y1, y2):
        """ Utilise l'approximation de Taylor (gradient et hessien) pour calculer le gain
        obtenu en séparant le nœud parent en deux nœuds enfants (y1 et y2). """
        # Séparation
        y, y_pred = self._split(y)
        y1, y1_pred = self._split(y1)
        y2, y2_pred = self._split(y2)

        true_gain = self._gain(y1, y1_pred)
        false_gain = self._gain(y2, y2_pred)
        gain = self._gain(y, y_pred)
        # Le gain total est le gain des enfants moins le gain du parent
        return true_gain + false_gain - gain

    def _approximate_update(self, y):
        """ Calcule le poids optimal de la feuille en utilisant la méthode de Newton (Gradient/Hessien). """
        # Séparation de y en y_vrai, y_pred
        y, y_pred = self._split(y)
        # Méthode de Newton
        gradient = np.sum(y * self.loss.gradient(y, y_pred), axis=0)
        hessian = np.sum(self.loss.hess(y, y_pred), axis=0)
        update_approximation =  gradient / hessian

        return update_approximation

    def fit(self, X, y):
        # Configuration des fonctions spécifiques à XGBoost avant l'entraînement
        self._impurity_calculation = self._gain_by_taylor
        self._leaf_value_calculation = self._approximate_update
        super(XGBoostRegressionTree, self).fit(X, y)


class RegressionTree(DecisionTree):
    """
    Arbre de Régression. Utilisé pour prédire des valeurs continues.
    L'impureté est mesurée par la variance (l'objectif est de regrouper des valeurs similaires).
    """
    def _calculate_variance_reduction(self, y, y1, y2):
        """ Calcule la réduction de variance (plus c'est grand, meilleure est la séparation). """
        var_tot = calculate_variance(y)
        var_1 = calculate_variance(y1)
        var_2 = calculate_variance(y2)
        frac_1 = len(y1) / len(y)
        frac_2 = len(y2) / len(y)

        # Calcul de la réduction de variance (Variance Initiale - Somme Pondérée des Variances des Enfants)
        variance_reduction = var_tot - (frac_1 * var_1 + frac_2 * var_2)

        return sum(variance_reduction)

    def _mean_of_y(self, y):
        """ La valeur d'une feuille en régression est simplement la moyenne des valeurs y de l'échantillon présent dans cette feuille. """
        value = np.mean(y, axis=0)
        return value if len(value) > 1 else value[0]

    def fit(self, X, y):
        self._impurity_calculation = self._calculate_variance_reduction
        self._leaf_value_calculation = self._mean_of_y
        super(RegressionTree, self).fit(X, y)

class ClassificationTree(DecisionTree):
    """
    Arbre de Classification. Utilisé pour prédire des étiquettes (catégories).
    L'impureté est mesurée par l'Entropie (Gain d'information).
    """
    def _calculate_information_gain(self, y, y1, y2):
        """ Calcule le gain d'information (baisse de l'entropie) résultant de la séparation. """
        # p représente la proportion d'échantillons allant dans la branche de gauche (y1)
        p = len(y1) / len(y)
        entropy = calculate_entropy(y) # Entropie avant séparation
        # Le gain d'information : Entropie Parent - Somme Pondérée de l'Entropie des Enfants
        info_gain = entropy - p * \
            calculate_entropy(y1) - (1 - p) * \
            calculate_entropy(y2)

        return info_gain

    def _majority_vote(self, y):
        """ Détermine l'étiquette la plus fréquente (Vote Majoritaire) pour la feuille. """
        most_common = None
        max_count = 0
        for label in np.unique(y):
            # Compte le nombre d'occurrences d'une étiquette (label) spécifique
            count = len(y[y == label])
            if count > max_count:
                most_common = label
                max_count = count
        return most_common

    def fit(self, X, y):
        self._impurity_calculation = self._calculate_information_gain
        self._leaf_value_calculation = self._majority_vote
        super(ClassificationTree, self).fit(X, y)
