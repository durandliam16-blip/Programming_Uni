/**
 * QUESTION 18 — Solution 2 : Le buffer gère LUI-MÊME deux puces distinctes.
 *
 * PRINCIPE :
 *   Contrairement à MemoireDouble (qui cache les deux puces derrière IMemoire),
 *   ici c'est le buffer lui-même qui sait qu'il a deux puces.
 *   Il gère la logique de bascule d'une puce à l'autre directement.
 *
 * DIFFÉRENCE avec la Solution 1 :
 *   Solution 1 (MemoireDouble) : transparence totale, BufferGen inchangé.
 *     → PRÉFÉRÉE car plus modulaire.
 *   Solution 2 (BufferDeuxPuces) : logique de bascule dans le buffer lui-même.
 *     → Plus complexe, mais peut être utile si les deux puces ont des comportements
 *       très différents (latences, types d'accès…).
 *
 * CONSEIL : En pratique, préférer la Solution 1 car elle respecte mieux
 * le principe de responsabilité unique (Single Responsibility Principle) :
 *   MemoireDouble s'occupe de "comment combiner les puces"
 *   BufferGen s'occupe de "comment gérer la file FIFO"
 */
class BufferDeuxPuces implements IFifo {

    private IMemoire puceA;
    private IMemoire puceB;
    private int tailleA;
    private int tailleB;
    private int tailleTotale;

    private int writePtr;
    private int readPtr;
    private int count;

    /**
     * @param puceA  première puce
     * @param tailleA taille en octets de la puce A
     * @param puceB  deuxième puce
     * @param tailleB taille en octets de la puce B
     */
    BufferDeuxPuces(IMemoire puceA, int tailleA, IMemoire puceB, int tailleB) {
        this.puceA = puceA;
        this.tailleA = tailleA;
        this.puceB = puceB;
        this.tailleB = tailleB;
        this.tailleTotale = tailleA + tailleB;
        this.writePtr = 0;
        this.readPtr  = 0;
        this.count    = 0;
    }

    /** Écrit un octet à l'adresse virtuelle "addr" (répartie sur les deux puces) */
    private void ecrire(int addr, byte val) {
        if (addr < tailleA) {
            puceA.set(addr, val);           // Adresse dans la puce A
        } else {
            puceB.set(addr - tailleA, val); // Adresse dans la puce B (offset soustrait)
        }
    }

    /** Lit un octet à l'adresse virtuelle "addr" */
    private byte lire(int addr) {
        if (addr < tailleA) {
            return puceA.get(addr);
        } else {
            return puceB.get(addr - tailleA);
        }
    }

    @Override
    public void enqueue(byte b) {
        if (isFull()) throw new RuntimeException("BufferDeuxPuces plein !");
        ecrire(writePtr, b);
        writePtr = (writePtr + 1) % tailleTotale;
        count++;
    }

    @Override
    public byte dequeue() {
        if (isEmpty()) throw new RuntimeException("BufferDeuxPuces vide !");
        byte val = lire(readPtr);
        readPtr = (readPtr + 1) % tailleTotale;
        count--;
        return val;
    }

    @Override
    public boolean isEmpty() { return count == 0; }

    @Override
    public boolean isFull() { return count == tailleTotale; }
}
