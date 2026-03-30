public class Cellule implements Liste {
    private int val;
    private Liste next;

    public Cellule(int val, Liste next) {
        this.val = val;
        this.next = next;
    }

    @Override
    public int longueur() {
        return 1 + next.longueur();
    }

    @Override
    public boolean contient(int n) {
        return (this.val == n) || next.contient(n);
    }

    @Override
    public int somme() {
        return this.val + next.somme();
    }

    @Override
    @Override
    public String toString() {
        return "Liste contenant " + this.longueur() + " element(s).";
    }

    // Méthodes type java.util.List
    @Override
    public boolean isEmpty() { return false; }
    @Override
    public int size() { return this.longueur(); }
    @Override
    public boolean contains(int n) { return this.contient(n); }
}