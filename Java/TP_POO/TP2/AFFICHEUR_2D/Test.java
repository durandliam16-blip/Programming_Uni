/**
 * QUESTION 5 & 6 : Classe Test — vérifie le fonctionnement de TextSimulator et Effects.
 *
 * QUESTION 5 — Vérification qu'aucune classe n'appelle l'autre :
 *   - TextSimulator.java : utilise IDisplay, IPoint, Intensite → PAS d'appel à Effects
 *   - Effects.java       : utilise IDisplay, Point, Intensite → PAS d'appel à TextSimulator
 *
 *   Ces deux classes ne se CONNAISSENT PAS mutuellement.
 *   Elles communiquent uniquement via l'interface IDisplay.
 *   C'est exactement le principe de la MODULARITÉ :
 *     → On peut remplacer TextSimulator par un vrai afficheur LED sans toucher à Effects.
 *     → On peut remplacer Effects par un autre pilote sans toucher à TextSimulator.
 *
 * QUESTION 6 — Classe Test :
 *   On "branche" un Effects sur un TextSimulator via IDisplay.
 *
 *   Schéma de connexion :
 *     [Effects (pilote)] ──IDisplay──> [TextSimulator (afficheur)]
 *
 *   COMPILATION : javac *.java
 *   EXÉCUTION   : java Test
 */
class Test {

    public static void main(String[] args) {

        // ── Étape 1 : Créer l'afficheur (TextSimulator implémente IDisplay)
        // On déclare la variable en type IDisplay (sous-typage) → meilleure pratique
        IDisplay afficheur = new TextSimulator(10, 20);
        // TextSimulator(lignes, colonnes) : crée un afficheur console 10×20
        // Le constructeur initialise et affiche un état aléatoire initial.

        System.out.println("=== État initial (aléatoire) affiché ci-dessus ===\n");

        // ── Étape 2 : Créer le pilote d'effets en lui passant l'afficheur
        // Effects ne sait PAS que c'est un TextSimulator — il voit juste un IDisplay.
        Effects effets = new Effects(afficheur);

        // ── Test 1 : Tout mettre à 0 (éteindre toutes les LED)
        System.out.println("=== Effet init(0) : tout éteindre ===");
        effets.init(new Intensite(0));

        // ── Test 2 : Tout mettre au maximum (allumer toutes les LED)
        System.out.println("=== Effet init(3) : tout allumer ===");
        effets.init(new Intensite(3));

        // ── Test 3 : Cercle de rayon 5
        System.out.println("=== Effet circle(5) : cercle de rayon 5 ===");
        effets.circle(5);

        // ── Test 4 : Cercle plus grand
        System.out.println("=== Effet circle(8) : cercle de rayon 8 ===");
        effets.circle(8);

        System.out.println("=== Tests terminés ===");
    }
}
