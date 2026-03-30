import java.util.NoSuchElementException ;
import java.io.PrintStream ;

public class BanqueMusique {
  
   public static class Sound{

      final String contenu ;

      Sound(String c) {contenu = c ; }
      
      @Override
      public String toString(){
         return "Sound with content :" + contenu ;
      }

      public void play(PrintStream out){
         out.print(this.toString());
      }

   }
   
   
   private BanqueMusique(){}
   
   
   /** Get music files based on their index.
       
       @exception Forbidden The requested file is not available in the country.
       
       @exception NoSuchElementException The requested file does not exist.
   */
   
   public static Sound getFile(int i) throws Forbidden {
      
      if (i==4) throw new Forbidden() ;
      if (i>10) throw new NoSuchElementException() ;
      
      return new Sound (Integer.toString(i)) ;
   }
   
   static final String messagePub = "Devenez membre Premium, c'est mieux !" ;
   
   public static Sound ajoutePublicite(Sound s){
      return new Sound (messagePub + " " +  s.contenu) ;
   }
   
} 
	
	
