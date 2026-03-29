/**
 * QUESTION 10 : Interface IFifo — contrat minimal pour une file d'attente (FIFO)
 *
 * FIFO = First In, First Out (Premier entré, Premier sorti)
 * Analogie : une file d'attente à la caisse — le premier arrivé est le premier servi.
 *
 * QUESTION 10 — Méthodes minimales d'une file d'attente :
 *   1. enqueue(byte b) : ajouter un élément en fin de file   (→ "enfiler")
 *   2. dequeue()       : retirer et retourner l'élément le plus ancien (→ "défiler")
 *   3. isEmpty()       : savoir si la file est vide (évite de défiler dans le vide)
 *   4. isFull()        : savoir si la file est pleine (évite d'écraser des données)
 *
 * QUESTION 11 — Pourquoi une interface plutôt qu'une classe ?
 *   → INDÉPENDANCE vis-à-vis du matériel : si le fabricant de la puce change,
 *     il suffit d'écrire une nouvelle classe qui implémente IFifo.
 *     Le code qui UTILISE la file d'attente (ex: l'affichage TV) ne change PAS.
 *   → TESTABILITÉ : on peut créer une implémentation de test simple (tableau Java)
 *     sans avoir besoin d'une vraie puce.
 *   → CONTRAT clair : l'interface documente exactement ce que la file doit faire.
 */
interface IFifo {

    /**
     * Ajoute un octet en fin de file (côté "entrée").
     * @param b l'octet à ajouter
     * @throws RuntimeException si la file est pleine
     */
    void enqueue(byte b);

    /**
     * Retire et retourne l'octet le plus ancien (côté "sortie").
     * @return le plus vieil octet non encore lu
     * @throws RuntimeException si la file est vide
     */
    byte dequeue();

    /**
     * @return true si la file ne contient aucun élément
     */
    boolean isEmpty();

    /**
     * @return true si la file est pleine (plus de place pour écrire)
     */
    boolean isFull();
}
