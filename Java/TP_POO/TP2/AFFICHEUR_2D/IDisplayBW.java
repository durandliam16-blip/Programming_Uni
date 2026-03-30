/**
 * QUESTION 8 : Interface IDisplayBW — afficheur binaire (noir/blanc).
 *
 * Interface d'un "vieil afficheur" qui ne connaît que deux états :
 *   - true  : diode allumée
 *   - false : diode éteinte
 *
 * Cette interface est DIFFÉRENTE d'IDisplay :
 *   IDisplay  : put(IPoint, Intensite)  — 4 niveaux de luminosité (0..3)
 *   IDisplayBW: put(int, int, boolean)  — 2 états (allumé/éteint)
 *
 * Pour brancher un pilote IDisplay sur cet afficheur, il faut un ADAPTATEUR
 * (voir Adaptateur42.java).
 */
interface IDisplayBW {

    /**
     * Allume ou éteint la diode à la position (x, y).
     * @param x     numéro de ligne
     * @param y     numéro de colonne
     * @param allume true = allumée, false = éteinte
     */
    void put(int x, int y, boolean allume);

    /**
     * @return le nombre de lignes de l'afficheur
     */
    int nbLignes();

    /**
     * @return le nombre de colonnes de l'afficheur
     */
    int nbColonnes();
}
