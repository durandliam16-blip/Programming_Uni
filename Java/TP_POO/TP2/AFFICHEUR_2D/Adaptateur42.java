/**
 * QUESTION 8 : Adaptateur42 — branche un pilote IDisplay sur un afficheur IDisplayBW.
 *
 * PROBLÈME :
 *   Le pilote (Effects) parle IDisplay  : put(IPoint, Intensite) avec 4 niveaux (0..3)
 *   Le vieil afficheur parle IDisplayBW : put(int, int, boolean) avec 2 états
 *   → Incompatibilité d'interface !
 *
 * SOLUTION — DESIGN PATTERN "Adapter" :
 *   Adaptateur42 IMPLÉMENTE IDisplay  → vu comme un afficheur normal par Effects
 *   Adaptateur42 CONTIENT un IDisplayBW → délègue vers le vrai afficheur après conversion
 *
 * SCHÉMA :
 *   [Effects (IDisplay)] ──IDisplay──> [Adaptateur42] ──IDisplayBW──> [Vieil afficheur]
 *
 * NOM "42" : IDisplay (4 niveaux) → IDisplayBW (2 états)
 *            4 → 2 d'où le suffixe "42"
 *
 * CONVERSION (4 niveaux → booléen) :
 *   Intensite 0 → false (éteint)
 *   Intensite 1, 2, 3 → true (allumé)
 *   Règle : si intensite > 0 → allumé, sinon → éteint
 */
class Adaptateur42 implements IDisplay {

    // L'afficheur binaire réel sur lequel on délègue
    private IDisplayBW cible;

    /**
     * @param cible l'afficheur IDisplayBW à piloter
     */
    Adaptateur42(IDisplayBW cible) {
        this.cible = cible;
    }

    /**
     * Reçoit un appel IDisplay (4 niveaux) et le convertit en appel IDisplayBW (booléen).
     *
     * CONVERSION : intensite > 0 → allumé (true), intensite == 0 → éteint (false)
     *
     * @param p point (ligne, colonne)
     * @param i intensité (0 à 3)
     */
    @Override
    public void put(IPoint p, Intensite i) {
        // Conversion : tout ce qui n'est pas 0 est considéré "allumé"
        boolean allume = (i.get() > 0);

        // Délégation à l'afficheur binaire avec la conversion
        cible.put(p.getX(), p.getY(), allume);
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
