class Reel extends Expression {
    private final double valeur;

    public Reel(double valeur) {
        this.valeur = valeur;
    }

    @Override
    public double eval() {
        return valeur;
    }
}