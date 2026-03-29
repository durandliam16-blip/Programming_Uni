/**
 * QUESTION 18 — Solution 1 : Deux puces vues comme UNE SEULE puce via un adaptateur.
 *
 * PRINCIPE (pattern "Adapter" / "Façade") :
 *   On crée une classe qui implémente IMemoire mais qui, en interne,
 *   utilise DEUX puces pour stocker les données.
 *   Le BufferGen ne voit qu'un seul IMemoire — il ne sait pas qu'il y a deux puces.
 *
 * MAPPING DES ADRESSES :
 *   Puce A (0 à tailleA-1)   → adresses 0 à tailleA-1
 *   Puce B (0 à tailleB-1)   → adresses tailleA à tailleA+tailleB-1
 *
 *   Exemple avec deux puces de 16 Mo :
 *   tailleA = 16 Mo = 16 777 216 octets
 *   Adresses 0 à 16 777 215   → puce A
 *   Adresses 16 777 216 à 33 554 431 → puce B
 *
 * USAge :
 *   IMemoire memDouble = new MemoireDouble(new Memoire32(), new Memoire32(), 16*1024*1024);
 *   BufferGen buf = new BufferGen(memDouble, 32*1024*1024);
 *
 * AVANTAGE de cette solution :
 *   BufferGen et IFifo ne changent pas du tout.
 *   On ajoute juste cette classe adaptateur.
 */
class MemoireDouble implements IMemoire {

    private IMemoire puceA;  // Première puce (adresses basses)
    private IMemoire puceB;  // Deuxième puce (adresses hautes)
    private int tailleA;     // Nombre d'octets dans la puce A (= point de bascule)

    /**
     * @param puceA  première puce mémoire
     * @param puceB  deuxième puce mémoire
     * @param tailleA nombre d'octets dans la puce A
     */
    MemoireDouble(IMemoire puceA, IMemoire puceB, int tailleA) {
        this.puceA  = puceA;
        this.puceB  = puceB;
        this.tailleA = tailleA;
    }

    /**
     * Écriture : on détermine dans quelle puce écrire selon l'adresse.
     */
    @Override
    public void set(int addr, byte val) {
        if (addr < tailleA) {
            // L'adresse est dans la plage de la puce A → écriture directe
            puceA.set(addr, val);
        } else {
            // L'adresse est dans la plage de la puce B → on soustrait l'offset
            puceB.set(addr - tailleA, val);
        }
    }

    /**
     * Lecture : même logique que set().
     */
    @Override
    public byte get(int addr) {
        if (addr < tailleA) {
            return puceA.get(addr);
        } else {
            return puceB.get(addr - tailleA);
        }
    }
}
