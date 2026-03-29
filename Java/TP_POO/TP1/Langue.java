/**
 * QUESTION 7 : Interface Java "Langue"
 *
 * Une INTERFACE en Java définit un CONTRAT : elle liste des méthodes
 * que toute classe "implémentant" cette interface DOIT fournir.
 * Elle ne contient PAS de code (pas de corps de méthode) — seulement des signatures.
 *
 * Pourquoi utiliser une interface plutôt qu'une classe ?
 *   → Flexibilité : on peut écrire du code qui fonctionne avec TOUTES les langues
 *     sans connaître leur implémentation concrète (French, Spanish, English…).
 *   → Modularité : on peut changer l'implémentation sans toucher au reste du code.
 *   → C'est le principe de "programmer vers une interface, pas vers une implémentation".
 */
interface Langue {

    /**
     * Retourne la traduction du mot "hello" dans cette langue.
     * Toute classe implémentant Langue DOIT fournir cette méthode.
     *
     * @return une chaîne de caractères correspondant à "hello"
     */
    String hello();
}
