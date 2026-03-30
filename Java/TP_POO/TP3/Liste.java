public interface Liste {
    int longueur();
    boolean contient(int n);
    int somme();
    
    // Pour la Question 6, 7, 8 (Compatibilité avec l'interface List de Java)
    boolean isEmpty();
    int size();
    boolean contains(int n);
}