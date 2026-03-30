import java.awt.Rectangle;

/**
 * QUESTION 1 & 2 : Classe Pulsar — palet animé qui grossit et rétrécit.
 *
 * ===== COMPARAISON DES DEUX SOLUTIONS (Question 1) =====
 *
 * SOLUTION 1 : Copier-coller de Palet puis modifier
 *   - Inconvénients :
 *     → Duplication de code : tout le code de déplacement/rebond est dupliqué.
 *     → Maintenance difficile : corriger un bug dans Palet oblige à aussi corriger Pulsar.
 *     → Si on veut 10 types de palets, on a 10 copies du même code.
 *     → Risque d'incohérences entre les copies.
 *   - Avantage : aucun (c'est une mauvaise pratique).
 *
 * SOLUTION 2 : Héritage (class Pulsar extends Palet) ← CHOISIE
 *   - Avantages :
 *     → Pulsar HÉRITE automatiquement de tout le code de Palet (déplacement, rebond).
 *     → On n'écrit QUE ce qui est différent (l'animation de taille).
 *     → Si on corrige Palet, Pulsar en bénéficie automatiquement.
 *     → Pulsar EST UN Palet → respecte le sous-typage (Liskov Substitution Principle).
 *   - Inconvénient mineur : couplage fort entre Pulsar et Palet (si Palet change beaucoup,
 *     Pulsar peut être impacté — mais c'est acceptable ici).
 *
 * ===== FONCTIONNEMENT DE L'ANIMATION =====
 *
 * Le palet pulse entre TAILLE_MIN et TAILLE_MAX pixels.
 * À chaque frame, la taille change de DELTA pixels.
 * Quand on atteint les limites, on inverse le sens (agrandir ↔ rétrécir).
 */
class Pulsar extends Palet {

    // Taille actuelle du carré (en pixels) — commence à la taille normale du Palet
    int tailleCourante;

    // Sens du changement de taille : +1 = grossit, -1 = rétrécit
    int sensAnimation;

    // Limites de l'animation
    static final int TAILLE_MIN = 4;
    static final int TAILLE_MAX = 24;

    // Vitesse d'animation : nombre de pixels ajoutés/retirés par frame
    static final int DELTA = 1;

    /**
     * Constructeur de Pulsar.
     *
     * Le mot-clé "super()" appelle le constructeur de Palet,
     * qui initialise x, y, dx, dy → on récupère tout gratuitement !
     * On n'a qu'à initialiser les attributs SPÉCIFIQUES à Pulsar.
     */
    Pulsar() {
        super();  // Appel du constructeur de Palet (initialise x, y, dx, dy)
        this.tailleCourante = Palet.TAILLE;  // On commence à la taille normale
        this.sensAnimation  = +1;            // On commence par grossir
    }

    /**
     * QUESTION 2 : Override de getRect() pour retourner la taille animée.
     *
     * @Override indique au compilateur qu'on redéfinit une méthode héritée.
     * Si la signature ne correspond pas à une méthode parente → erreur de compilation.
     * C'est une bonne pratique : ça documente l'intention et évite les fautes de frappe.
     *
     * super.getRect() retournerait le Rectangle de Palet (taille fixe = 10).
     * On construit notre propre Rectangle avec tailleCourante à la place.
     *
     * On centre l'animation sur le centre du palet original pour que
     * le palet ne "saute" pas visuellement lors des changements de taille.
     */
    @Override
    public Rectangle getRect() {
        // Calcul du décalage pour centrer le Pulsar sur la position du Palet
        int offset = (tailleCourante - Palet.TAILLE) / 2;
        return new Rectangle(
            this.x - offset,          // On décale x pour centrer
            this.y - offset,          // On décale y pour centrer
            tailleCourante,           // Largeur animée
            tailleCourante            // Hauteur animée
        );
    }

    /**
     * QUESTION 2 : Override de deplace() pour ajouter l'animation à chaque frame.
     *
     * On RÉUTILISE le comportement de Palet avec "super.deplace()" (déplacement + rebond),
     * puis on AJOUTE le comportement supplémentaire (animation de taille).
     *
     * C'est le principe de l'héritage : étendre sans réécrire.
     */
    @Override
    public void deplace() {
        // 1. On délègue le déplacement à Palet (rebond, mise à jour x/y)
        super.deplace();

        // 2. On met à jour la taille animée
        tailleCourante += sensAnimation * DELTA;

        // 3. Si on atteint une limite, on inverse le sens
        if (tailleCourante >= TAILLE_MAX) {
            tailleCourante = TAILLE_MAX;
            sensAnimation  = -1;  // On commence à rétrécir
        } else if (tailleCourante <= TAILLE_MIN) {
            tailleCourante = TAILLE_MIN;
            sensAnimation  = +1;  // On commence à grossir
        }
    }
}
