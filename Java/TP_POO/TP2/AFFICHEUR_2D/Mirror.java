/**
 * QUESTION 7 : Classe Mirror — filtre d'inversion horizontale.
 *
 * RÔLE : Se brancher ENTRE un pilote (Effects) et un afficheur (TextSimulator).
 *        Intercepte chaque appel put(point, intensite) et renvoie le pixel
 *        à la colonne SYMÉTRIQUE (inversion horizontale, comme un miroir).
 *
 * SCHÉMA DE CONNEXION :
 *   [Effects (pilote)] ──IDisplay──> [Mirror (filtre)] ──IDisplay──> [TextSimulator]
 *
 * Mirror IMPLÉMENTE IDisplay → vu comme un afficheur par Effects.
 * Mirror CONTIENT un IDisplay → il délègue les appels vers l'afficheur réel.
 * C'est le DESIGN PATTERN "Decorator" (ou "Proxy") :
 *   on ajoute un comportement (l'inversion) sans modifier ni le pilote ni l'afficheur.
 *
 * SPÉCIFICATION DU CONSTRUCTEUR (demandée par la question) :
 *   Mirror(IDisplay cible) — reçoit l'afficheur sur lequel on va déléguer.
 *
 * SPÉCIFICATION DE LA MÉTHODE put :
 *   void put(IPoint p, Intensite i)
 *   Reçoit un point (x, y), calcule la colonne miroir y' = nbColonnes - 1 - y,
 *   et transmet put(Point(x, y'), i) à l'afficheur cible.
 *
 * EXEMPLE (afficheur 5 colonnes, colonnes 0..4) :
 *   Colonne originale : 0  1  2  3  4
 *   Colonne miroir    : 4  3  2  1  0   (symétrie par rapport au centre)
 *   Formule : colonne_miroir = nbColonnes - 1 - colonne_originale
 */
class Mirror implements IDisplay {

    // L'afficheur "derrière" le miroir — on va lui déléguer les appels transformés
    private IDisplay cible;

    /**
     * Constructeur — reçoit l'afficheur cible (injection de dépendance).
     * @param cible l'afficheur réel sur lequel Mirror va déléguer
     */
    Mirror(IDisplay cible) {
        this.cible = cible;
    }

    /**
     * Met à jour un pixel avec INVERSION HORIZONTALE.
     *
     * Transformation : la colonne y devient (nbColonnes - 1 - y)
     * La ligne x reste inchangée (on n'inverse que horizontalement).
     *
     * @param p     point original (ligne x, colonne y)
     * @param i     intensité lumineuse
     */
    @Override
    public void put(IPoint p, Intensite i) {
        // Calcul de la colonne symétrique
        int colonneOriginale = p.getY();
        int colonneMiroir    = cible.nbColonnes() - 1 - colonneOriginale;

        // On crée un nouveau point avec la colonne inversée (la ligne x ne change pas)
        IPoint pointMiroir = new Point(p.getX(), colonneMiroir);

        // On délègue à l'afficheur cible avec le point transformé
        cible.put(pointMiroir, i);
    }

    /**
     * Mirror a les MÊMES dimensions que l'afficheur cible.
     * Il se comporte comme un afficheur de même taille.
     */
    @Override
    public int nbLignes() {
        return cible.nbLignes();
    }

    @Override
    public int nbColonnes() {
        return cible.nbColonnes();
    }
}
