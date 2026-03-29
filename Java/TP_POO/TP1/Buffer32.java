/**
 * QUESTION 12 : Mémoire tampon FIFO utilisant une puce Memoire32.
 *
 * PRINCIPE DU BUFFER CIRCULAIRE :
 *   On imagine la mémoire comme un cercle.
 *   - Le pointeur d'écriture (writePtr) avance à chaque enqueue().
 *   - Le pointeur de lecture (readPtr) avance à chaque dequeue().
 *   - Quand un pointeur atteint la fin, il repart au début (modulo).
 *   - Tant que writePtr ≠ readPtr (et que la file n'est pas pleine),
 *     les données sont dans l'ordre d'insertion.
 *
 *  [0][1][2]...[readPtr]...[writePtr]...[33554431]
 *        ^                 ^
 *    prochain à lire   prochain à écrire
 *
 * QUESTION 13 : Combien de lignes changer pour une autre puce ?
 *   → Toutes les occurrences de "Memoire32" dans ce fichier (type du champ + constructeur).
 *   Solution propre : utiliser IMemoire à la place (voir BufferGen).
 */
class Buffer32 implements IFifo {

    // QUESTION 13 : Ici on utilise Memoire32 directement — couplage fort.
    // Si on veut changer de puce, il faut modifier ce type ET le constructeur.
    private Memoire32 puce;

    // Taille totale disponible (nombre d'octets dans la puce)
    private static final int TAILLE = Memoire32.TAILLE;

    // Pointeur d'écriture : adresse où on va écrire le PROCHAIN octet entrant
    private int writePtr;

    // Pointeur de lecture : adresse du plus vieil octet pas encore lu
    private int readPtr;

    // Nombre d'octets actuellement stockés dans la file
    // Nécessaire pour distinguer "file vide" (count=0) de "file pleine" (count=TAILLE)
    // car dans les deux cas writePtr == readPtr !
    private int count;

    /**
     * Constructeur : reçoit la puce mémoire en paramètre (injection de dépendance).
     * On initialise les deux pointeurs à 0 et le compteur à 0 (file vide).
     *
     * @param puce la puce Memoire32 à utiliser comme stockage
     */
    Buffer32(Memoire32 puce) {
        this.puce = puce;
        this.writePtr = 0;  // On commence à écrire depuis l'adresse 0
        this.readPtr  = 0;  // On commence à lire depuis l'adresse 0
        this.count    = 0;  // La file est vide au départ
    }

    /**
     * QUESTION 12 : Ajoute un octet en fin de file.
     *
     * Étapes :
     * 1. Vérifier que la file n'est pas pleine.
     * 2. Écrire l'octet à l'adresse writePtr.
     * 3. Avancer writePtr (avec wrap-around circulaire via modulo).
     * 4. Incrémenter le compteur.
     *
     * @param b l'octet à ajouter
     */
    @Override
    public void enqueue(byte b) {
        if (isFull()) {
            throw new RuntimeException("Buffer plein ! Impossible d'ajouter un octet.");
        }
        // Écriture de l'octet à la position courante du pointeur d'écriture
        puce.set(writePtr, b);

        // Avancer le pointeur d'écriture de façon circulaire :
        // quand on atteint la fin (adresse TAILLE-1), on repart à 0.
        writePtr = (writePtr + 1) % TAILLE;

        count++;  // Un octet de plus dans la file
    }

    /**
     * QUESTION 12 : Retire et retourne l'octet le plus ancien.
     *
     * Étapes :
     * 1. Vérifier que la file n'est pas vide.
     * 2. Lire l'octet à l'adresse readPtr.
     * 3. Avancer readPtr (circulaire).
     * 4. Décrémenter le compteur.
     * 5. Retourner l'octet lu.
     *
     * @return l'octet le plus ancien (premier entré)
     */
    @Override
    public byte dequeue() {
        if (isEmpty()) {
            throw new RuntimeException("Buffer vide ! Impossible de lire un octet.");
        }
        // Lire l'octet à la position du pointeur de lecture
        byte valeur = puce.get(readPtr);

        // Avancer le pointeur de lecture de façon circulaire
        readPtr = (readPtr + 1) % TAILLE;

        count--;  // Un octet de moins dans la file

        return valeur;
    }

    /** @return true si la file ne contient aucun octet */
    @Override
    public boolean isEmpty() {
        return count == 0;
    }

    /** @return true si la file est complètement remplie (plus d'espace) */
    @Override
    public boolean isFull() {
        return count == TAILLE;
    }

    /** @return le nombre d'octets actuellement dans la file */
    public int size() {
        return count;
    }
}
