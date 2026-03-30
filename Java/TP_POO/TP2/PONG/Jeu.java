import javax.swing.*;
import java.awt.*;

/**
 * Fenêtre principale du jeu Pong.
 *
 * MODIFICATION par rapport à la version originale :
 *   - new Palet() remplacé par new Pulsar() (Question 3)
 */
class MaFenetre extends JFrame {

    JPanel pan;

    MaFenetre() {
        setSize(320, 200 + 50);  // +50 pour la barre de titre de l'OS
        // QUESTION 3 : on remplace new Palet() par new Pulsar()
        // Possible grâce au sous-typage : Pulsar EST UN MovingObject (via Palet)
        pan = new Paneau(new Pulsar());
        setContentPane(pan);
    }
}

/**
 * Panneau de dessin — affiche le palet à chaque repaint().
 *
 * MODIFICATION par rapport à la version originale :
 *   Avant : g.fillRect(p.getX(), p.getY(), 10, 10)
 *   Maintenant : on utilise p.getRect() qui retourne un Rectangle complet.
 *
 * POURQUOI ce changement est meilleur ?
 *   - getRect() retourne aussi la TAILLE → le panneau n'a plus besoin de savoir
 *     que le palet fait "10x10". C'est le palet lui-même qui décide de sa taille.
 *   - Pour Pulsar, la taille change à chaque frame → avec l'ancienne méthode,
 *     il aurait fallu ajouter getWidth() et getHeight() à l'interface.
 *   - Un seul appel au lieu de deux → moins de risque d'incohérence.
 */
class Paneau extends JPanel {

    MovingObject p;  // Type interface, pas Palet ni Pulsar → flexible

    Paneau(MovingObject p) {
        super();
        this.p = p;
    }

    @Override
    public void paintComponent(Graphics g) {
        // Efface l'arrière-plan avant de redessiner (évite les "fantômes")
        super.paintComponent(g);

        // On récupère le Rectangle du palet (position + taille)
        Rectangle r = p.getRect();

        // On dessine le carré à la position et avec la taille du Rectangle
        g.fillRect(r.x, r.y, r.width, r.height);

        // On déplace le palet pour la prochaine frame
        p.deplace();
    }
}

/**
 * QUESTION 3 : Point d'entrée du jeu.
 *
 * Boucle principale : toutes les 50ms (~20 FPS), on demande un repaint().
 * Swing appelle alors paintComponent() qui redessine et déplace le palet.
 */
public class Jeu {

    public static void main(String[] args) throws InterruptedException {

        System.setProperty("sun.java2d.opengl", "true"); // Animation fluide (OpenGL)

        MaFenetre fen = new MaFenetre();
        fen.setVisible(true);
        fen.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Boucle de jeu : repaint toutes les 50ms
        while (true) {
            fen.repaint();
            Thread.sleep(50);
        }
    }
}