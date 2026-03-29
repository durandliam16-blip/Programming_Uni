/**
 * QUESTION 4, 9 : Classe Message — exploite le sous-typage via l'interface Langue
 *
 * ÉVOLUTION du code :
 *   Q4 : Message avait un champ String et un constructeur sans paramètre.
 *   Q6 : Message utilisait directement un objet French (couplage fort).
 *   Q9 : Message utilise maintenant l'interface Langue (couplage faible).
 *
 * AVANTAGE du sous-typage (Q9) :
 *   La classe Message ne connaît plus la classe French.
 *   Elle travaille avec n'importe quelle Langue (French, Spanish, English…).
 *   On peut changer de langue sans modifier Message — seulement Hello.java change.
 *
 * C'est le principe d'ENCAPSULATION et d'INVERSION DE DÉPENDANCE :
 *   on dépend de l'abstraction (Langue), pas de l'implémentation (French).
 */
class Message {

    // QUESTION 9 : Le champ est de type Langue (l'interface), pas French (la classe concrète).
    // Cela permet à Message de fonctionner avec TOUTE classe implémentant Langue.
    private Langue langue;

    /**
     * QUESTION 9 : Le constructeur reçoit un objet Langue en paramètre.
     * C'est le principe d'INJECTION DE DÉPENDANCE :
     * on "injecte" la dépendance depuis l'extérieur plutôt que de la créer ici.
     *
     * Avantage : Message n'est plus responsable de CRÉER une langue,
     * il reçoit juste celle qu'on lui donne.
     *
     * @param langue n'importe quel objet implémentant l'interface Langue
     */
    Message(Langue langue) {
        this.langue = langue;  // "this.langue" = le champ de l'objet, "langue" = le paramètre
    }

    /**
     * Affiche le message dans la langue configurée.
     * Appelle la méthode hello() de l'interface — sans savoir quelle langue concrète c'est.
     */
    void print() {
        // langue.hello() appelle la méthode de l'objet réel (French, Spanish, etc.)
        // C'est le POLYMORPHISME : le comportement dépend du type réel de l'objet.
        System.out.println(this.langue.hello());
    }
}
