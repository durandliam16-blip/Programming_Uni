import java.awt.Rectangle;

/**
 * Interface MovingObject — décrit tout objet mobile dans le jeu Pong.
 *
 * ÉVOLUTION par rapport à l'ancienne version :
 *   Avant : getX() et getY() renvoyaient deux int séparés
 *   Maintenant : getRect() renvoie un Rectangle complet
 *
 * POURQUOI ce changement ?
 *   Un Rectangle encapsule x, y, largeur ET hauteur.
 *   Cela prépare des évolutions futures : collisions, objets de tailles différentes,
 *   zones de détection… sans avoir à changer l'interface à nouveau.
 *
 * Toute classe implémentant MovingObject DOIT fournir :
 *   - getRect() : position et dimensions actuelles de l'objet
 *   - deplace() : mise à jour de la position (appelée à chaque frame)
 */
interface MovingObject {

    /**
     * Retourne la position et la taille de l'objet sous forme de Rectangle.
     * @return un Rectangle AWT (x, y, largeur, hauteur)
     */
    java.awt.Rectangle getRect();

    /**
     * Déplace l'objet d'une étape (appelée ~20 fois/seconde par la boucle de jeu).
     */
    void deplace();
}