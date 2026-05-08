class Addition extends Expression {
    private final Expression gauche;
    private final Expression droite;

    public Addition(Expression gauche, Expression droite) {
        this.gauche = gauche;
        this.droite = droite;
    }

    @Override
    public double eval() {
        // Évaluation récursive
        return gauche.eval() + droite.eval();
    }
}