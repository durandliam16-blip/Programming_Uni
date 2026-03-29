import javax.swing.* ;
import java.awt.* ;


class MaFenetre extends JFrame {

   JPanel pan ;

   MaFenetre(){
      setSize(320,200+50);
      pan = new Paneau(new Palet()) ;
      setContentPane(pan) ;
   }
}



class Paneau extends JPanel {

   MovingObject p ;

   Paneau(MovingObject p){
      super();
      this.p=p ;
   }

   @Override
   public void paintComponent (Graphics g){
      g.fillRect (p.getX(),p.getY(),10,10);
      p.deplace() ;
   }
}



public class Jeu {

   public static void main(String[] args) throws InterruptedException {

      System.setProperty("sun.java2d.opengl", "true"); /* pour animation fluide */

      MaFenetre fen = new MaFenetre() ;

      fen.setVisible(true);

      fen.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      
      while (true){
         fen.repaint() ; 
         Thread.sleep(50);
      }

   }
}
