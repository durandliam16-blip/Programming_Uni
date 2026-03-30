public class Vide implements Liste {
    @Override
    public int longueur() { return 0; }

    @Override
    public boolean contient(int n) { return false; }

    @Override
    public int somme() { return 0; }

    @Override
    public String toString() {
        return "Liste contenant " + this.longueur() + " element(s).";
    }

    // Méthodes type java.util.List
    @Override
    public boolean isEmpty() { return true; }
    @Override
    public int size() { return this.longueur(); }
    @Override
    public boolean contains(int n) { return this.contient(n); }
}