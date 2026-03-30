import java.awt.Rectangle;

/**
 * Classe Palet — un carré mobile qui rebondit dans la fenêtre.
 *
 * Implémente l'interface MovingObject via getRect() (et non plus getX/getY).
 *
 * PHYSIQUE SIMPLE :
 *   Le palet a une vitesse (dx, dy) en pixels par frame.
 *   À chaque appel de deplace(), on déplace le palet.
 *   Quand il touche un bord, on inverse la composante de vitesse correspondante.
 *
 * DIMENSIONS de la fenêtre : 320 x 200 (taille définie dans MaFenetre).
 * TAILLE du carré : 10 x 10 pixels.
 */
class Palet implements MovingObject {

    // Position du coin supérieur gauche du carré
    int x;
    int y;

    // Vitesse en pixels par frame (peut être négative = mouvement vers la gauche/haut)
    int dx;
    int dy;

    // Dimensions de la fenêtre (limites de rebond)
    static final int LARGEUR_FENETRE = 320;
    static final int HAUTEUR_FENETRE = 200;

    // Taille du carré représentant le palet
    static final int TAILLE = 10;

    /**
     * Constructeur : initialise le palet au centre de la fenêtre
     * avec une vitesse diagonale de 3 pixels/frame.
     */
    Palet() {
        this.x  = LARGEUR_FENETRE / 2;
        this.y  = HAUTEUR_FENETRE / 2;
        this.dx = 3;   // 3 pixels vers la droite par frame
        this.dy = 2;   // 2 pixels vers le bas par frame
    }

    /**
     * QUESTION 1 → QUESTION 2 :
     * Retourne la position et taille du palet sous forme de Rectangle.
     * C'est la méthode centrale de l'interface MovingObject.
     *
     * new Rectangle(x, y, largeur, hauteur)
     *   x, y      : coin supérieur gauche
     *   largeur, hauteur : dimensions
     */
    @Override
    public Rectangle getRect() {
        return new Rectangle(this.x, this.y, TAILLE, TAILLE);
    }

    /**
     * Déplace le palet d'une étape et gère les rebonds sur les bords.
     *
     * LOGIQUE DE REBOND :
     *   Si le palet sort par la droite  (x + TAILLE > LARGEUR) → inverser dx
     *   Si le palet sort par la gauche  (x < 0)                → inverser dx
     *   Si le palet sort par le bas     (y + TAILLE > HAUTEUR) → inverser dy
     *   Si le palet sort par le haut    (y < 0)                → inverser dy
     */
    @Override
    public void deplace() {
        // Déplacement
        x += dx;
        y += dy;

        // Rebond horizontal : bord droit ou gauche
        if (x + TAILLE > LARGEUR_FENETRE || x < 0) {
            dx = -dx;  // Inversion de la vitesse horizontale
            // On recadre pour ne pas "sortir" du cadre
            x = Math.max(0, Math.min(x, LARGEUR_FENETRE - TAILLE));
        }

        // Rebond vertical : bord bas ou haut
        if (y + TAILLE > HAUTEUR_FENETRE || y < 0) {
            dy = -dy;  // Inversion de la vitesse verticale
            y = Math.max(0, Math.min(y, HAUTEUR_FENETRE - TAILLE));
        }
    }
}