public class Main {
    public static void main(String[] args) {
        System.out.println("--- Validation de l'API d'Expression ---");

        // Test Question 2 : Addition classique
        Expression e1 = new Addition(new Entier(2), new Entier(3));
        System.out.println("Test classique (2 + 3) : " + e1.eval()); // Attendu: 5.0

        // Test Question 3 : API Fluide (Surcharge et chaînage)
        Expression e2 = new Entier(2).add(3).add(4.5);
        System.out.println("Test API Fluide (2 + 3 + 4.5) : " + e2.eval()); // Attendu: 9.5

        // Test Question 4 : Extension Multiplication
        // (2 + 3) * 4
        Expression e3 = new Entier(2).add(3).mul(4);
        System.out.println("Test Mixte ((2 + 3) * 4) : " + e3.eval()); // Attendu: 20.0

        // Test complexe : 2 * 3 + 4 * 5
        Expression eComplex = new Entier(2).mul(3).add(new Entier(4).mul(5));
        System.out.println("Test Complexe (2*3 + 4*5) : " + eComplex.eval()); // Attendu: 26.0
    }
}