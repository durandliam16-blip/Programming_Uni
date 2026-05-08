class Entier extends Expression {
    private final int valeur;

    public Entier(int valeur) {
        this.valeur = valeur;
    }

    @Override
    public double eval() {
        return (double) valeur;
    }
}