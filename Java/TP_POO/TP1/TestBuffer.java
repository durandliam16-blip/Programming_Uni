/**
 * QUESTION 12 : Jeu de tests pour Buffer32 et BufferGen.
 *
 * Cette classe contient la méthode main et effectue plusieurs tests.
 * Chaque test vérifie un comportement précis de la file d'attente.
 *
 * COMPILATION : javac *.java
 * EXÉCUTION   : java TestBuffer
 *
 * BONNE PRATIQUE : les tests sont dans une classe séparée de l'implémentation.
 * En 4e année, vous utiliserez JUnit pour écrire des tests automatisés.
 */
class TestBuffer {

    // Compteur pour suivre le nombre de tests passés / échoués
    static int testsTotal  = 0;
    static int testsReussis = 0;

    /**
     * Méthode utilitaire : vérifie une condition et affiche le résultat.
     * @param nom       nom du test (pour identifier l'échec)
     * @param condition doit être true pour que le test passe
     */
    static void verifier(String nom, boolean condition) {
        testsTotal++;
        if (condition) {
            testsReussis++;
            System.out.println("  ✓ " + nom);
        } else {
            System.out.println("  ✗ ÉCHEC : " + nom);
        }
    }

    public static void main(String[] args) {

        // =========================================================
        // TESTS DE Buffer32 (puce Memoire32 — Question 12)
        // =========================================================
        System.out.println("=== Tests Buffer32 (Memoire32) ===");

        Memoire32 puce32 = new Memoire32();
        Buffer32 buf32 = new Buffer32(puce32);

        // Test 1 : file vide au départ
        verifier("File vide au départ", buf32.isEmpty());
        verifier("File non pleine au départ", !buf32.isFull());
        verifier("Taille 0 au départ", buf32.size() == 0);

        // Test 2 : enqueue d'un seul octet
        buf32.enqueue((byte) 42);
        verifier("Après enqueue(42) : non vide", !buf32.isEmpty());
        verifier("Après enqueue(42) : taille = 1", buf32.size() == 1);

        // Test 3 : dequeue retourne le bon octet (FIFO)
        byte lu = buf32.dequeue();
        verifier("dequeue retourne 42", lu == 42);
        verifier("Après dequeue : vide à nouveau", buf32.isEmpty());

        // Test 4 : ordre FIFO avec plusieurs octets
        buf32.enqueue((byte) 10);
        buf32.enqueue((byte) 20);
        buf32.enqueue((byte) 30);
        verifier("FIFO : premier sorti = 10", buf32.dequeue() == 10);
        verifier("FIFO : deuxième sorti = 20", buf32.dequeue() == 20);
        verifier("FIFO : troisième sorti = 30", buf32.dequeue() == 30);
        verifier("File vide après tout défiler", buf32.isEmpty());

        // Test 5 : valeurs négatives (les bytes Java sont signés : -128 à 127)
        buf32.enqueue((byte) -1);
        buf32.enqueue((byte) -128);
        buf32.enqueue((byte) 127);
        verifier("Byte négatif -1", buf32.dequeue() == -1);
        verifier("Byte min -128", buf32.dequeue() == -128);
        verifier("Byte max 127", buf32.dequeue() == 127);

        // Test 6 : exception si dequeue sur file vide
        boolean exceptionLevee = false;
        try {
            buf32.dequeue();  // Devrait lever une exception
        } catch (RuntimeException e) {
            exceptionLevee = true;
        }
        verifier("Exception sur dequeue vide", exceptionLevee);

        // =========================================================
        // TESTS DE BufferGen avec Memoire32 (Question 14)
        // =========================================================
        System.out.println("\n=== Tests BufferGen avec Memoire32 ===");

        // On crée un BufferGen avec une puce Memoire32.
        // Notez : on passe l'objet en tant que IMemoire (sous-typage).
        IMemoire mem32 = new Memoire32();
        BufferGen bufGen32 = new BufferGen(mem32, Memoire32.TAILLE);

        bufGen32.enqueue((byte) 1);
        bufGen32.enqueue((byte) 2);
        bufGen32.enqueue((byte) 3);
        verifier("BufferGen/Memoire32 : FIFO 1", bufGen32.dequeue() == 1);
        verifier("BufferGen/Memoire32 : FIFO 2", bufGen32.dequeue() == 2);
        verifier("BufferGen/Memoire32 : FIFO 3", bufGen32.dequeue() == 3);
        verifier("BufferGen/Memoire32 : vide après", bufGen32.isEmpty());

        // =========================================================
        // TESTS DE BufferGen avec Puce64 (Question 14 — 2e puce)
        // =========================================================
        System.out.println("\n=== Tests BufferGen avec Puce64 ===");

        // QUESTION 15 : On change juste ces deux lignes — BufferGen lui-même ne change pas !
        IMemoire mem64 = new Puce64();
        BufferGen bufGen64 = new BufferGen(mem64, Puce64.TAILLE);

        bufGen64.enqueue((byte) 100);
        bufGen64.enqueue((byte) 50);
        verifier("BufferGen/Puce64 : FIFO 100", bufGen64.dequeue() == 100);
        verifier("BufferGen/Puce64 : FIFO 50", bufGen64.dequeue() == 50);
        verifier("BufferGen/Puce64 : vide après", bufGen64.isEmpty());

        // =========================================================
        // TEST DU WRAP-AROUND CIRCULAIRE (Question 12)
        // =========================================================
        System.out.println("\n=== Test wrap-around circulaire ===");

        // On utilise un petit buffer (5 octets) pour tester le wrap-around
        // sans attendre d'écrire 33 millions d'octets.
        // On simule avec un tableau Java dans une classe anonyme.
        IMemoire petiteMem = new IMemoire() {
            byte[] data = new byte[5];
            public void set(int addr, byte val) { data[addr] = val; }
            public byte get(int addr) { return data[addr]; }
        };

        BufferGen petit = new BufferGen(petiteMem, 5);

        // Remplissage complet
        petit.enqueue((byte) 1);
        petit.enqueue((byte) 2);
        petit.enqueue((byte) 3);
        petit.enqueue((byte) 4);
        petit.enqueue((byte) 5);
        verifier("Buffer plein après 5 enqueues", petit.isFull());

        // Vider partiellement
        petit.dequeue(); // retire 1
        petit.dequeue(); // retire 2

        // Remplir à nouveau (le writePtr doit faire un wrap-around)
        petit.enqueue((byte) 6);  // writePtr revient à 0 (wrap)
        petit.enqueue((byte) 7);  // writePtr = 1

        // Vérifier l'ordre FIFO après wrap
        verifier("Wrap-around : ordre 3", petit.dequeue() == 3);
        verifier("Wrap-around : ordre 4", petit.dequeue() == 4);
        verifier("Wrap-around : ordre 5", petit.dequeue() == 5);
        verifier("Wrap-around : ordre 6", petit.dequeue() == 6);
        verifier("Wrap-around : ordre 7", petit.dequeue() == 7);
        verifier("Buffer vide après wrap-around", petit.isEmpty());

        // =========================================================
        // TESTS QUESTION 18 — MemoireDouble (Solution 1)
        // =========================================================
        System.out.println("\n=== Tests MemoireDouble (Q18 - Solution 1) ===");

        int moitie = 16 * 1024 * 1024; // 16 Mo par puce
        IMemoire double32 = new MemoireDouble(new Memoire32(), new Memoire32(), moitie);
        BufferGen bufDouble = new BufferGen(double32, moitie * 2);

        bufDouble.enqueue((byte) 11);
        bufDouble.enqueue((byte) 22);
        verifier("MemoireDouble FIFO 11", bufDouble.dequeue() == 11);
        verifier("MemoireDouble FIFO 22", bufDouble.dequeue() == 22);
        verifier("MemoireDouble vide", bufDouble.isEmpty());

        // =========================================================
        // TESTS QUESTION 18 — BufferDeuxPuces (Solution 2)
        // =========================================================
        System.out.println("\n=== Tests BufferDeuxPuces (Q18 - Solution 2) ===");

        BufferDeuxPuces buf2 = new BufferDeuxPuces(
            new Memoire32(), Memoire32.TAILLE,
            new Puce64(),    Puce64.TAILLE
        );

        buf2.enqueue((byte) 55);
        buf2.enqueue((byte) 66);
        verifier("BufferDeuxPuces FIFO 55", buf2.dequeue() == 55);
        verifier("BufferDeuxPuces FIFO 66", buf2.dequeue() == 66);
        verifier("BufferDeuxPuces vide", buf2.isEmpty());

        // =========================================================
        // BILAN
        // =========================================================
        System.out.println("\n=== Bilan ===");
        System.out.println(testsReussis + " / " + testsTotal + " tests réussis.");
        if (testsReussis == testsTotal) {
            System.out.println("Tous les tests sont passés !");
        } else {
            System.out.println("Des tests ont échoué — vérifiez votre implémentation.");
        }
    }
}
