/**
 * Simulation d'une puce mémoire 32 mégaoctets.
 *
 * Cette classe simule le fonctionnement d'une vraie puce hardware.
 * En réalité, ce serait du code natif communiquant avec le matériel.
 * Ici, on utilise simplement un tableau Java pour stocker les octets.
 *
 * La puce NE SAIT PAS :
 *   - ce qu'on stocke dedans (images, texte, son…)
 *   - si une case est "vide" ou "pleine"
 *   - l'ordre d'écriture des données
 *   Elle n'expose que deux opérations primitives : lire et écrire un octet.
 *
 * QUESTION 13 : Si on veut utiliser une puce d'un autre fabricant,
 *   on doit modifier Buffer32 partout où Memoire32 est mentionné.
 *   Solution : utiliser l'interface IMemoire (voir BufferGen).
 */
class Memoire32 implements IMemoire {

    // 32 Mo = 32 × 1024 × 1024 = 33 554 432 octets
    // C'est une constante (static final) : la taille ne change jamais.
    static final int TAILLE = 33_554_432;  // Le _ est juste pour la lisibilité (Java 7+)

    // Le tableau qui simule la puce physique.
    // En Java, un tableau de byte est initialisé à 0 automatiquement.
    private byte[] memoire;

    /**
     * Constructeur : alloue la "puce" (le tableau de 32 Mo).
     */
    Memoire32() {
        this.memoire = new byte[TAILLE];
    }

    /**
     * Lit un octet à l'adresse donnée.
     * @param addr adresse entre 0 et TAILLE-1
     * @return l'octet stocké à cette adresse
     */
    @Override
    public byte get(int addr) {
        return memoire[addr];
    }

    /**
     * Écrit un octet à l'adresse donnée.
     * Si une valeur y était déjà, elle est écrasée.
     * @param addr adresse entre 0 et TAILLE-1
     * @param val  octet à écrire
     */
    @Override
    public void set(int addr, byte val) {
        memoire[addr] = val;
    }
}
