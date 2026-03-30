public class Test {
    public static void main(String[] args) {
        Liste maListe = new Cellule(2, new Cellule(4, new Vide()));

        System.out.println("Longueur : " + maListe.longueur()); // Affiche 2
        System.out.println("Contient 5 ? " + maListe.contient(5)); // false
        System.out.println("Contient 4 ? " + maListe.contient(4)); // true
        
        // Test Question 4.3
        System.out.print(maListe); 
    }
}