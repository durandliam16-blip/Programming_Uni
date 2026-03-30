import java.util.ArrayList;
import java.util.List;

public class Systeme {
    private List<Utilisateur> abonnés;

    public Systeme() {
        this.abonnés = new ArrayList<>();
    }

    public void ajouterUtilisateur(Utilisateur u) {
        this.abonnés.add(u);
    }

    // Facturation mensuelle [cite: 110, 126]
    public void payeTous() {
        for (Utilisateur u : abonnés) {
            if (!u.facturer()) {
                System.out.println("Échec de transaction pour un utilisateur."); // [cite: 111]
            }
        }
    }

    // Réinitialisation quotidienne [cite: 116, 126]
    public void resetTous() {
        for (Utilisateur u : abonnés) {
            u.reset();
        }
    }
}