/**
 * Tests des Questions 7, 8, 9 : Mirror, Adaptateur42, Adaptateur24.
 *
 * COMPILATION : javac *.java
 * EXÉCUTION   : java TestAdaptateurs
 */
class TestAdaptateurs {

    public static void main(String[] args) {

        // ── QUESTION 7 : Test de Mirror ──────────────────────────────────────
        System.out.println("=== Q7 : Mirror (inversion horizontale) ===");
        System.out.println("--- Afficheur direct (sans Mirror) ---");

        IDisplay afficheur = new TextSimulator(5, 10);
        Effects effets = new Effects(afficheur);
        effets.circle(4);

        System.out.println("--- Même effet via Mirror (image inversée) ---");

        // On branche Mirror ENTRE Effects et TextSimulator
        // Effects → Mirror → TextSimulator
        IDisplay miroir = new Mirror(new TextSimulator(5, 10));
        Effects effetsMiroir = new Effects(miroir);
        effetsMiroir.circle(4);
        // Le cercle doit apparaître symétrique horizontalement


        // ── QUESTION 8 : Test d'Adaptateur42 ────────────────────────────────
        System.out.println("\n=== Q8 : Adaptateur42 (IDisplay → IDisplayBW) ===");

        // Simulateur d'afficheur binaire (pour le test)
        IDisplayBW afficheurBW = new SimulateurBW(5, 10);

        // On branche un pilote IDisplay (Effects) sur l'afficheur binaire via l'adaptateur
        IDisplay adapter42 = new Adaptateur42(afficheurBW);
        Effects effets42 = new Effects(adapter42);
        effets42.circle(3);
        // Les intensités > 0 s'affichent comme 'X' (allumé), 0 s'affiche comme ' '


        // ── QUESTION 9 : Test d'Adaptateur24 ────────────────────────────────
        System.out.println("\n=== Q9 : Adaptateur24 (IDisplayBW → IDisplay) ===");

        // Un "pilote binaire" qui allume les pixels d'une diagonale
        IDisplay afficheur24 = new TextSimulator(5, 10);
        IDisplayBW adapter24 = new Adaptateur24(afficheur24);

        // Simulation d'un pilote binaire : allume la diagonale
        System.out.println("Pilote binaire : diagonale allumée");
        for (int i = 0; i < 5; i++) {
            adapter24.put(i, i, true);   // diagonale allumée
            adapter24.put(i, i+1, false); // voisin éteint
        }

        System.out.println("\n=== Tous les tests terminés ===");
    }
}

/**
 * Simulateur d'afficheur binaire (noir/blanc) pour les tests.
 * Affiche 'X' pour allumé et ' ' pour éteint.
 */
class SimulateurBW implements IDisplayBW {

    boolean[][] grille;
    int nbl, nbc;

    SimulateurBW(int l, int c) {
        this.nbl = l;
        this.nbc = c;
        this.grille = new boolean[l][c];
        afficher();
    }

    @Override
    public void put(int x, int y, boolean allume) {
        grille[x][y] = allume;
        afficher();
    }

    @Override
    public int nbLignes()   { return nbl; }

    @Override
    public int nbColonnes() { return nbc; }

    void afficher() {
        StringBuilder sb = new StringBuilder();
        for (boolean[] ligne : grille) {
            for (boolean b : ligne) {
                sb.append(b ? 'X' : ' ');
                sb.append(' ');
            }
            sb.append('\n');
        }
        System.out.println(sb);
    }
}
