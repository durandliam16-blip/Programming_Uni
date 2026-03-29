/**
 * QUESTION 1, 2 : Première classe Java — point d'entrée du programme.
 *
 * En Java, chaque programme démarre par la méthode `main`.
 * Sa signature est OBLIGATOIRE : public static void main(String[] args)
 *   - public  : accessible de partout
 *   - static  : appartient à la classe, pas à un objet (on n'a pas besoin de créer un Hello)
 *   - void    : ne retourne rien
 *   - String[] args : tableau des arguments passés en ligne de commande
 *
 * COMPILATION : javac Hello.java
 * EXÉCUTION   : java Hello
 */

// QUESTION 9 : main adapté pour exploiter l'interface Langue (sous-typage)
class Hello {

    public static void main(String[] args) {

        // On crée un objet French, mais on le stocke dans une variable de type Langue.
        // C'est le SOUS-TYPAGE : French "est une" Langue, donc c'est valide.
        // Avantage : si on veut utiliser une autre langue (Spanish, English…),
        // on change SEULEMENT cette ligne. Le reste du code ne change pas.
        Langue maLangue = new French();

        // On passe l'objet Langue au constructeur de Message.
        // Message ne sait pas que c'est un French — il voit juste un Langue.
        Message monMessage = new Message(maLangue);

        // Appel de la méthode print() : affichera "bonjour"
        monMessage.print();
    }
}
