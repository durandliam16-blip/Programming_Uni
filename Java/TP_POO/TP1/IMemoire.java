/**
 * QUESTION 14 : Interface IMemoire — contrat commun pour toutes les puces mémoire
 *
 * Cette interface est fournie par le fabricant de puces.
 * Elle garantit que TOUTES les puces proposent les mêmes deux opérations de base.
 *
 * POURQUOI une interface ?
 *   → Si on code directement avec Memoire32, on est lié à ce fabricant.
 *   → Avec IMemoire, on peut brancher n'importe quelle puce sans changer notre code.
 *   → C'est le principe OUVERT/FERMÉ : ouvert à l'extension (nouvelles puces),
 *     fermé à la modification (pas besoin de changer BufferGen).
 */
public interface IMemoire {

    /**
     * Écrit un octet (byte) à l'adresse donnée.
     * Aucune garantie de comportement si addr est hors des limites.
     *
     * @param addr adresse mémoire (entier positif)
     * @param val  octet à écrire (valeur entre -128 et 127 en Java)
     */
    void set(int addr, byte val);

    /**
     * Lit l'octet stocké à l'adresse donnée.
     * Aucune garantie de comportement si addr est hors des limites.
     *
     * @param addr adresse mémoire (entier positif)
     * @return l'octet lu à cette adresse
     */
    byte get(int addr);
}
