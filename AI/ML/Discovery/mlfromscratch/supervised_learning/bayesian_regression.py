from __future__ import print_function, division
import numpy as np
from scipy.stats import chi2, multivariate_normal
from mlfromscratch.utils import mean_squared_error, train_test_split, polynomial_features


class BayesianRegression(object):
    """Modèle de Régression Bayésienne. 
    Si 'poly_degree' (degré polynomial) est spécifié, les caractéristiques (features) seront
    transformées avec une fonction de base polynomiale, ce qui permet de faire de la régression polynomiale.
    
    Ce modèle suppose :
    - Une distribution a priori (prior) Normale pour les poids (weights).
    - Une distribution a priori Chi-carré inverse mise à l'échelle (scaled inverse chi-squared) 
      pour la variance des poids.
    
    Le but de l'inférence bayésienne ici n'est pas seulement de trouver un seul jeu de poids optimal,
    mais de trouver la distribution de probabilité des poids (postérieurs) en combinant nos croyances 
    initiales (a priori) avec les données observées (vraisemblance).

    Paramètres:
    -----------
    n_draws: float
        Le nombre de tirages simulés à partir de la distribution a posteriori des paramètres.
    mu0: array
        Les valeurs moyennes (mean) de la distribution Normale a priori des paramètres (poids).
    omega0: array
        La matrice de précision (inverse de la matrice de covariance) de la distribution Normale a priori.
    nu0: float
        Les degrés de liberté (degrees of freedom) de la distribution Chi-carré inverse a priori.
    sigma_sq0: float
        Le paramètre d'échelle (scale) de la distribution Chi-carré inverse a priori.
    poly_degree: int
        Le degré du polynôme pour la transformation des caractéristiques.
    cred_int: float
        L'intervalle de crédibilité (Credible Interval, équivalent bayésien de l'intervalle de confiance). 
        Par exemple, 95 => intervalle de crédibilité à 95% pour les paramètres.

    Référence:
        https://github.com/mattiasvillani/BayesLearnCourse/raw/master/Slides/BayesLearnL5.pdf
    """
    def __init__(self, n_draws, mu0, omega0, nu0, sigma_sq0, poly_degree=0, cred_int=95):
        self.w = None
        self.n_draws = n_draws
        self.poly_degree = poly_degree
        self.cred_int = cred_int

        # Paramètres a priori (prior parameters)
        self.mu0 = mu0
        self.omega0 = omega0
        self.nu0 = nu0
        self.sigma_sq0 = sigma_sq0

    # Permet de simuler (tirer des valeurs) à partir d'une distribution Chi-carré inverse.
    # On suppose que la variance (sigma carré) suit cette distribution.
    # Référence:
    #   https://en.wikipedia.org/wiki/Scaled_inverse_chi-squared_distribution
    def _draw_scaled_inv_chi_sq(self, n, df, scale):
        # 1. Tirer d'une distribution Chi-carré classique
        X = chi2.rvs(size=n, df=df)
        # 2. Appliquer la transformation pour obtenir la version "inverse" et "mise à l'échelle"
        sigma_sq = df * scale / X
        return sigma_sq

    def fit(self, X, y):

        # Si une transformation polynomiale est demandée
        if self.poly_degree:
            X = polynomial_features(X, degree=self.poly_degree)

        n_samples, n_features = np.shape(X)

        # X^T * X (souvent utilisé dans les calculs matriciels de régression)
        X_X = X.T.dot(X)

        # Approximation des Moindres Carrés (Least Squares) de Beta (les poids)
        # Formule : Beta = (X^T * X)^-1 * X^T * y
        beta_hat = np.linalg.pinv(X_X).dot(X.T).dot(y)

        # -------------------------------------------------------------------------
        # Les paramètres a posteriori (postérieurs) peuvent être déterminés analytiquement 
        # car nous supposons des "a priori conjugués" (conjugate priors) pour nos vraisemblances.
        # Cela signifie que l'a posteriori appartient à la même famille de distribution que l'a priori.
        # -------------------------------------------------------------------------

        # Prior Normal + Vraisemblance Normale => Posterior Normal
        # Formule pour la nouvelle moyenne (mu_n) : Combine l'estimateur classique (beta_hat) avec l'a priori (mu0)
        mu_n = np.linalg.pinv(X_X + self.omega0).dot(X_X.dot(beta_hat) + self.omega0.dot(self.mu0))
        
        # Nouvelle matrice de précision (omega_n) : Somme de la précision des données et de l'a priori
        omega_n = X_X + self.omega0
        
        # Prior Chi-carré inverse + Vraisemblance => Posterior Chi-carré inverse
        # Nouveaux degrés de liberté : on ajoute simplement le nombre d'observations
        nu_n = self.nu0 + n_samples
        
        # Nouveau paramètre d'échelle (sigma_sq_n)
        # C'est une mise à jour complexe qui combine l'erreur résiduelle (y^T y) avec l'impact des priors
        sigma_sq_n = (1.0 / nu_n) * (self.nu0 * self.sigma_sq0 + \
            (y.T.dot(y) + self.mu0.T.dot(self.omega0).dot(self.mu0) - mu_n.T.dot(omega_n.dot(mu_n))))

        # -------------------------------------------------------------------------
        # Simulation (Échantillonnage)
        # -------------------------------------------------------------------------
        # Nous tirons des valeurs de paramètres simulées (n_draws fois) à partir de notre distribution a posteriori
        beta_draws = np.empty((self.n_draws, n_features))
        for i in range(self.n_draws):
            # 1. On tire une variance à partir de l'a posteriori Chi-carré inverse
            sigma_sq = self._draw_scaled_inv_chi_sq(n=1, df=nu_n, scale=sigma_sq_n)
            
            # 2. Connaissant cette variance, on tire un vecteur de poids (Beta) depuis l'a posteriori Normal Multivarié
            # La matrice de covariance est : sigma_sq * (omega_n)^-1
            beta = multivariate_normal.rvs(size=1, mean=mu_n[:, 0], cov=sigma_sq * np.linalg.pinv(omega_n))
            
            # Sauvegarde du tirage
            beta_draws[i, :] = beta

        # -------------------------------------------------------------------------
        # Décision finale
        # -------------------------------------------------------------------------
        # Nous choisissons la moyenne (mean) des variables simulées comme poids (w)
        # qui seront utilisés pour faire nos prédictions finales.
        self.w = np.mean(beta_draws, axis=0)

        # Calcul des limites inférieure et supérieure de l'intervalle de crédibilité (Credible Interval)
        # Ex : pour 95%, l_eti = 2.5% (percentile 2.5) et u_eti = 97.5% (percentile 97.5)
        l_eti = 50 - self.cred_int / 2
        u_eti = 50 + self.cred_int / 2
        
        # On calcule les percentiles pour chaque caractéristique (feature)
        self.eti = np.array([[np.percentile(beta_draws[:, i], q=l_eti), np.percentile(beta_draws[:, i], q=u_eti)] \
                                for i in range(n_features)])

    def predict(self, X, eti=False):

        # Appliquer la transformation polynomiale si nécessaire
        if self.poly_degree:
            X = polynomial_features(X, degree=self.poly_degree)

        # La prédiction est le produit scalaire standard : y = X * w
        y_pred = X.dot(self.w)
        
        # Si on a demandé de retourner les limites de l'intervalle de crédibilité
        if eti:
            lower_w = self.eti[:, 0]
            upper_w = self.eti[:, 1]
            # Prédictions avec les poids "pessimistes" (limite basse) et "optimistes" (limite haute)
            y_lower_pred = X.dot(lower_w)
            y_upper_pred = X.dot(upper_w)
            return y_pred, y_lower_pred, y_upper_pred

        return y_pred
