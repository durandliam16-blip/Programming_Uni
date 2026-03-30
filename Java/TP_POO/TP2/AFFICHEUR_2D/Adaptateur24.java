/**
 * QUESTION 9 : Adaptateur24 — branche un pilote IDisplayBW sur un afficheur IDisplay.
 *
 * C'est l'INVERSE d'Adaptateur42 :
 *   Le pilote (binaire) parle IDisplayBW : put(int, int, boolean)
 *   Le nouvel afficheur parle IDisplay  : put(IPoint, Intensite) avec 4 niveaux
 *
 * SCHÉMA :
 *   [Pilote binaire (IDisplayBW)] ──IDisplayBW──> [Adaptateur24] ──IDisplay──> [TextSimulator]
 *
 * NOM "24" : IDisplayBW (2 états) → IDisplay (4 niveaux)
 *            2 → 4 d'où le suffixe "24"
 *
 * CONVERSION (booléen → 4 niveaux) :
 *   true  (allumé) → Intensite(3)  (luminosité maximale)
 *   false (éteint) → Intensite(0)  (éteint)
 *
 * REMARQUE :
 *   On perd de l'information avec Adaptateur42 (4→2 : les niveaux 1 et 2 sont traités comme 3).
 *   On ne gagne pas d'information avec Adaptateur24 (2→4 : on ne peut pas "deviner" les niveaux 1 et 2).
 *   C'est inévitable : un canal avec moins d'information ne peut pas en créer.
 */
class Adaptateur24 implements IDisplayBW {

    // L'afficheur IDisplay réel (4 niveaux) sur lequel on délègue
    private IDisplay cible;

    /**
     * @param cible l'afficheur IDisplay à piloter (ex: TextSimulator)
     */
    Adaptateur24(IDisplay cible) {
        this.cible = cible;
    }

    /**
     * Reçoit un appel IDisplayBW (booléen) et le convertit en appel IDisplay (Intensite).
     *
     * CONVERSION :
     *   true  → Intensite(3) : maximum de luminosité
     *   false → Intensite(0) : éteint
     *
     * @param x      numéro de ligne
     * @param y      numéro de colonne
     * @param allume état de la diode
     */
    @Override
    public void put(int x, int y, boolean allume) {
        // Conversion booléen → Intensite
        Intensite intensite = allume ? new Intensite(3) : new Intensite(0);

        // Création du point et délégation à l'afficheur IDisplay
        IPoint point = new Point(x, y);
        cible.put(point, intensite);
    }

    @Override
    public int nbLignes() {
        return cible.nbLignes();
    }

    @Override
    public int nbColonnes() {
        return cible.nbColonnes();
    }
}
