/**
 * QUESTION 6, 8 : Classe French — implémente l'interface Langue
 *
 * Le mot-clé "implements Langue" indique que French s'engage à respecter
 * le contrat de l'interface Langue. Le compilateur vérifie que la méthode
 * hello() est bien présente — sinon il produit une erreur de compilation.
 *
 * QUESTION 6 : Problème de compilation en cascade
 *   Si on compile seulement Hello.java, Java recompile ses dépendances DIRECTES
 *   (Message), mais pas les dépendances de dépendances (French).
 *   Résultat : modifier French.java sans recompiler explicitement
 *   ne produit PAS d'effet visible à l'exécution.
 *   Solution : utiliser un outil de build (make, maven, gradle) qui gère
 *   automatiquement l'arbre de dépendances complet.
 */
class French implements Langue {

    /**
     * QUESTION 8 : Implémentation concrète de la méthode de l'interface.
     * Le compilateur vérifie que la signature correspond EXACTEMENT
     * à celle déclarée dans l'interface (String hello()).
     *
     * @return "bonjour" — traduction française de "hello"
     */
    @Override  // Annotation optionnelle mais recommandée : confirme qu'on implémente bien l'interface
    public String hello() {
        return "bonjour";
    }
}
