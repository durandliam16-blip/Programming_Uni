class Multiplication extends Expression {
    private final Expression gauche;
    private final Expression droite;

    public Multiplication(Expression gauche, Expression droite) {
        this.gauche = gauche;
        this.droite = droite;
    }

    @Override
    public double eval() {
        return gauche.eval() * droite.eval();
    }
}