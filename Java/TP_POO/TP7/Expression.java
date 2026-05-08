public abstract class Expression {
    // Méthode d'évaluation que chaque sous-classe doit implémenter
    public abstract double eval();

    // --- API FLUIDE POUR L'ADDITION ---

    // Ajout d'une autre expression
    public Expression add(Expression e) {
        return new Addition(this, e);
    }

    // Surcharge pour les entiers : évite la duplication en réutilisant add(Expression)
    public Expression add(int val) {
        return this.add(new Entier(val));
    }

    // Surcharge pour les réels
    public Expression add(double val) {
        return this.add(new Reel(val));
    }

    // --- API FLUIDE POUR LA MULTIPLICATION ---

    public Expression mul(Expression e) {
        return new Multiplication(this, e);
    }

    public Expression mul(int val) {
        return this.mul(new Entier(val));
    }

    public Expression mul(double val) {
        return this.mul(new Reel(val));
    }
}