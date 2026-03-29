/**
 * QUESTION 14 : Mémoire tampon FIFO générique — utilise IMemoire au lieu de Memoire32.
 *
 * DIFFÉRENCE avec Buffer32 :
 *   Buffer32  → dépend de Memoire32  (couplage FORT, 1 seul fabricant possible)
 *   BufferGen → dépend de IMemoire  (couplage FAIBLE, N fabricants possibles)
 *
 * QUESTION 15 : Combien de lignes modifier pour changer de puce ?
 *   → ZÉRO ligne dans BufferGen !
 *   On change seulement le code qui CRÉE le BufferGen (le main dans TestBuffer).
 *   Exemple :
 *     new BufferGen(new Memoire32(), Memoire32.TAILLE)   ← puce 32 Mo
 *     new BufferGen(new Puce64(),    Puce64.TAILLE)      ← puce 64 Mo
 *   BufferGen lui-même ne change pas du tout.
 *
 * QUESTION 17 — Propriété de la modularité :
 *   On peut remplacer un module (BufferGen.class) sans recompiler les modules qui l'utilisent
 *   (TestBuffer.class), tant que l'interface (IFifo) reste la même.
 *   → Séparation compilation / déploiement
 *   → Travail en équipe facilité : chaque équipe livre son .class
 */
class BufferGen implements IFifo {

    // QUESTION 14 : Type IMemoire — compatible avec Memoire32, Puce64, et toute future puce.
    private IMemoire puce;

    // Taille de la puce passée en paramètre (on ne la connaît pas à l'avance)
    private int taille;

    // Pointeur d'écriture : adresse du prochain octet entrant
    private int writePtr;

    // Pointeur de lecture : adresse du plus vieil octet pas encore consommé
    private int readPtr;

    // Nombre d'octets actuellement dans la file
    private int count;

    /**
     * Constructeur générique.
     * On reçoit la puce ET sa taille (car IMemoire n'expose pas de méthode size()).
     *
     * @param puce   n'importe quel objet implémentant IMemoire
     * @param taille nombre total d'octets disponibles sur cette puce
     */
    BufferGen(IMemoire puce, int taille) {
        this.puce   = puce;
        this.taille = taille;
        this.writePtr = 0;
        this.readPtr  = 0;
        this.count    = 0;
    }

    /**
     * Ajoute un octet en fin de file (FIFO).
     * Le buffer circulaire : quand writePtr atteint la fin, il repart à 0.
     */
    @Override
    public void enqueue(byte b) {
        if (isFull()) {
            throw new RuntimeException("BufferGen plein !");
        }
        puce.set(writePtr, b);
        writePtr = (writePtr + 1) % taille;  // Wrap-around circulaire
        count++;
    }

    /**
     * Retire et retourne le plus vieil octet de la file.
     */
    @Override
    public byte dequeue() {
        if (isEmpty()) {
            throw new RuntimeException("BufferGen vide !");
        }
        byte valeur = puce.get(readPtr);
        readPtr = (readPtr + 1) % taille;  // Wrap-around circulaire
        count--;
        return valeur;
    }

    @Override
    public boolean isEmpty() {
        return count == 0;
    }

    @Override
    public boolean isFull() {
        return count == taille;
    }

    public int size() {
        return count;
    }
}
