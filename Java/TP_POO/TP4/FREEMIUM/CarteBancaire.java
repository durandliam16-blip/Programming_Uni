/* Pour les accents : javadoc -public -charset utf8 CarteBancaire.java */

public class CarteBancaire{

    int numero;
    int date;
    int pictogramme;

    public CarteBancaire(int numero, int date, int pictogramme){
	this.numero = numero ;
	this.date = date ;
	this.pictogramme = pictogramme ;
    }

    /** Déclenche un paiement sur cette carte.
	@return Le booléen renvoyé indique si la transaction a réussi ou échoué.
    */
    public boolean paye(int montant){
       if (montant > 0 && montant < 500){
          System.out.println ("Carte numero " + this.numero + " : debit " + montant +".") ;
          return true ; 
       }
       else return false ;
    }

}

