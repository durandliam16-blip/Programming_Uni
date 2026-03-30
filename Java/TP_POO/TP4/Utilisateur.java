import java.util.ArrayList;
import java.util.List;

public class Utilisateur {
    private final int id;
    private final String nom;
    private List<Integer> favoris;
    private CarteBancaire cb;
    private Statut statutActuel;

    public Utilisateur(int id, String nom, CarteBancaire cb) {
        this.id = id;
        this.nom = nom;
        this.cb = cb;
        this.favoris = new ArrayList<>();
        this.statutActuel = new StatutGratuit(); // Par défaut [cite: 100]
    }

    // --- Gestion du changement de statut ---
    public void devenirPremium() {
        this.statutActuel = new StatutPremium(); // [cite: 107]
    }

    public void redevenirGratuit() {
        this.statutActuel = new StatutGratuit(); // [cite: 108]
    }

    // --- Actions déléguées au statut ---
    public BanqueMusique.Sound ecouter(int idMorceau) throws Forbidden {
        return statutActuel.ecouter(idMorceau); // [cite: 102]
    }

    public boolean facturer() {
        return statutActuel.payer(this.cb); // [cite: 110]
    }

    public void reset() {
        statutActuel.reset(); // [cite: 116]
    }

    // --- Classe interne Abstraite pour le Statut ---
    private abstract class Statut {
        abstract BanqueMusique.Sound ecouter(int idMorceau) throws Forbidden;
        abstract boolean payer(CarteBancaire cb);
        abstract void reset();
    }

    // --- Sous-classe : Utilisateur Gratuit ---
    private class StatutGratuit extends Statut {
        private int compteur = 0;
        private final int LIMITE = 3; // [cite: 105, 112]

        @Override
        BanqueMusique.Sound ecouter(int idMorceau) throws Forbidden {
            if (compteur < LIMITE) {
                compteur++;
                return BanqueMusique.getFile(idMorceau); // [cite: 117]
            } else {
                System.out.println("Limite atteinte. Passez en Premium !");
                return null;
            }
        }

        @Override
        boolean payer(CarteBancaire cb) { return true; } // Gratuit, rien à payer

        @Override
        void reset() { this.compteur = 0; }
    }

    // --- Sous-classe : Utilisateur Premium ---
    private class StatutPremium extends Statut {
        private final int TARIF = 10; // [cite: 110, 113]

        @Override
        BanqueMusique.Sound ecouter(int idMorceau) throws Forbidden {
            return BanqueMusique.getFile(idMorceau); // Illimité [cite: 106]
        }

        @Override
        boolean payer(CarteBancaire cb) {
            return cb.paye(TARIF); // [cite: 123]
        }

        @Override
        void reset() { /* Pas de compteur à réinitialiser */ }
    }
}