/**
 * Simulation d'une puce mémoire 64 mégaoctets — second fabricant.
 *
 * QUESTION 14 : Cette classe implémente IMemoire, comme Memoire32.
 * Cela permet à BufferGen d'utiliser l'une ou l'autre sans rien changer.
 *
 * En pratique, une "vraie" Puce64 serait fournie par un fabricant différent
 * et pourrait fonctionner différemment en interne (mémoire flash, DRAM, etc.).
 * Notre code (BufferGen) n'a pas besoin de le savoir — il utilise juste IMemoire.
 */
class Puce64 implements IMemoire {

    // 64 Mo = 64 × 1024 × 1024 = 67 108 864 octets
    static final int TAILLE = 67_108_864;

    private byte[] memoire;

    Puce64() {
        this.memoire = new byte[TAILLE];
    }

    @Override
    public byte get(int addr) {
        return memoire[addr];
    }

    @Override
    public void set(int addr, byte val) {
        memoire[addr] = val;
    }
}
