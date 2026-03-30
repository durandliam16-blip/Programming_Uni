# TP n°2 — POO Java : Interfaces (suite)
## Héritage, Decorator, Adapter — INFO3/IDIA3 Polytech Nantes

---

## Structure des fichiers

```
tp2/
├── ── SECTION 1 : Jeu Pong ──────────────────────────────────────────────────
├── MovingObject.java      # Interface avec getRect() + deplace()
├── Palet.java             # Carré mobile, implémente MovingObject
├── Pulsar.java            # Q1-2 : Palet animé (héritage de Palet)
├── Jeu.java               # Q3 : Point d'entrée Swing, modifié pour getRect() + Pulsar
│
├── ── SECTION 2 : Afficheur 2D ──────────────────────────────────────────────
├── IDisplay.java          # Interface afficheur (fourni)
├── IDisplayBW.java        # Q8 : Interface afficheur binaire (noir/blanc)
├── IPoint.java            # Interface point (fourni)
├── Point.java             # Implémentation d'IPoint (fourni)
├── Intensite.java         # Valeur de luminosité 0..3 (fourni)
├── TextSimulator.java     # Simulateur console d'afficheur (fourni)
├── Effects.java           # Pilote d'effets visuels (fourni)
│
├── Test.java              # Q6 : Teste Effects + TextSimulator ensemble
├── Mirror.java            # Q7 : Filtre d'inversion horizontale
├── Adaptateur42.java      # Q8 : Adapte IDisplay → IDisplayBW
├── Adaptateur24.java      # Q9 : Adapte IDisplayBW → IDisplay
└── TestAdaptateurs.java   # Tests des Q7, Q8, Q9
```

---

## Commandes

```bash
# Tout compiler
javac *.java

# Section 2 — Test afficheur + effets (Q6)
java Test

# Section 2 — Test Mirror + Adaptateurs (Q7-9)
java TestAdaptateurs

# Section 1 — Jeu Pong avec Pulsar (Q3) — nécessite un écran graphique
java Jeu
```

---

## Réponses aux questions

---

### Section 1 — Jeu Pong

**Q1 — Comparaison des deux solutions pour Pulsar**

| Critère | Solution 1 : Copier-coller | Solution 2 : Héritage ✓ |
|---|---|---|
| Duplication de code | Oui (tout Palet recopié) | Non (réutilisé via `super`) |
| Correction de bug | À faire 2 fois | Une seule fois dans Palet |
| Cohérence | Risque d'incohérence | Garantie par héritage |
| Extensibilité | Difficile (N palets = N copies) | Facile |
| Sous-typage | Pulsar n'est pas un Palet | Pulsar EST un Palet (et un MovingObject) |

**→ Héritage obligatoire.** Le copier-coller est toujours une mauvaise pratique en POO.

---

**Q2 — Code de Pulsar (spécialisation par héritage)**

```java
class Pulsar extends Palet {

    int tailleCourante = Palet.TAILLE;
    int sensAnimation  = +1;  // +1 = grossit, -1 = rétrécit

    Pulsar() {
        super();  // appelle le constructeur de Palet (x, y, dx, dy initialisés)
    }

    @Override
    public Rectangle getRect() {
        // On centre l'animation sur la position du Palet
        int offset = (tailleCourante - Palet.TAILLE) / 2;
        return new Rectangle(x - offset, y - offset, tailleCourante, tailleCourante);
    }

    @Override
    public void deplace() {
        super.deplace();           // délègue le déplacement à Palet
        tailleCourante += sensAnimation;
        if (tailleCourante >= 24) sensAnimation = -1;
        if (tailleCourante <= 4)  sensAnimation = +1;
    }
}
```

Points clés :
- `extends Palet` → Pulsar hérite de tous les champs et méthodes de Palet
- `super()` → appelle le constructeur parent (obligatoire en 1ère ligne)
- `super.deplace()` → réutilise le comportement de déplacement/rebond sans le réécrire
- `@Override` → le compilateur vérifie qu'on redéfinit bien une méthode existante

---

**Q3 — Modification de Jeu.java**

Deux changements :
```java
// 1. Dans MaFenetre : new Palet() → new Pulsar()
pan = new Paneau(new Pulsar());

// 2. Dans paintComponent : getX()/getY() → getRect()
Rectangle r = p.getRect();
g.fillRect(r.x, r.y, r.width, r.height);
// On peut maintenant dessiner n'importe quelle taille, pas seulement 10x10
```

---

### Section 2 — Afficheur 2D

**Q4 — Comparaison des 4 interfaces pour `put`**

| Interface | Avantages | Inconvénients |
|---|---|---|
| `put(int, int, int)` | Simple, peu de classes | Pas de vérification de type (on peut passer n'importe quel int) |
| `put(Point, int)` | Coordonnées groupées | Intensité non contrôlée (pas de range 0..3) |
| `put(int, int, Intensite)` | Intensité contrôlée | Coordonnées séparées, pas réutilisables |
| `put(IPoint, Intensite)` ✓ | Typage fort des deux paramètres, extensible | Légèrement plus verbose |

**→ `put(IPoint, Intensite)` est préférable** : les deux paramètres sont typés, le compilateur vérifie les valeurs, et IPoint/Intensite peuvent avoir plusieurs implémentations.

---

**Q5 — Effects et TextSimulator ne se connaissent pas**

En cherchant dans les sources :
- `TextSimulator.java` : imports `java.util.Random` → **aucune référence à Effects**
- `Effects.java` : utilise `IDisplay`, `Point`, `Intensite` → **aucune référence à TextSimulator**

Les deux classes communiquent **uniquement via l'interface IDisplay**.
C'est exactement le principe de couplage faible.

---

**Q6 — Classe Test : brancher Effects sur TextSimulator**

```java
IDisplay afficheur = new TextSimulator(10, 20);  // L'afficheur
Effects effets = new Effects(afficheur);          // Le pilote

effets.init(new Intensite(0));   // Tout éteindre
effets.init(new Intensite(3));   // Tout allumer
effets.circle(5);                // Cercle de rayon 5
```

Schéma : `[Effects] ──IDisplay──> [TextSimulator]`

---

**Q7 — Classe Mirror : filtre d'inversion horizontale**

**Spécification :**
- Constructeur : `Mirror(IDisplay cible)` — reçoit l'afficheur à "encadrer"
- Méthode put : `void put(IPoint p, Intensite i)` — transforme la colonne avant de déléguer

**Transformation :**
```
colonne_miroir = nbColonnes - 1 - colonne_originale
```
Exemple sur 10 colonnes (0..9) :
```
Original : 0  1  2  3  4  5  6  7  8  9
Miroir   : 9  8  7  6  5  4  3  2  1  0
```

**Code :**
```java
class Mirror implements IDisplay {
    private IDisplay cible;

    Mirror(IDisplay cible) { this.cible = cible; }

    @Override
    public void put(IPoint p, Intensite i) {
        int colonneMiroir = cible.nbColonnes() - 1 - p.getY();
        cible.put(new Point(p.getX(), colonneMiroir), i);
    }
    // nbLignes() et nbColonnes() délèguent à cible
}
```

Utilisation : `Effects → Mirror → TextSimulator`
```java
IDisplay miroir = new Mirror(new TextSimulator(5, 10));
new Effects(miroir).circle(4);
```

C'est le **Design Pattern Decorator** : on ajoute un comportement (l'inversion) sans modifier le pilote ni l'afficheur.

---

**Q8 — Adaptateur42 : IDisplay → IDisplayBW**

Problème : le pilote parle IDisplay (4 niveaux), le vieil afficheur parle IDisplayBW (booléen).

```
[Effects (IDisplay)] ──IDisplay──> [Adaptateur42] ──IDisplayBW──> [Vieil afficheur]
```

Conversion : `intensite > 0 → true (allumé)`, `intensite == 0 → false (éteint)`

```java
class Adaptateur42 implements IDisplay {
    private IDisplayBW cible;

    Adaptateur42(IDisplayBW cible) { this.cible = cible; }

    @Override
    public void put(IPoint p, Intensite i) {
        boolean allume = (i.get() > 0);          // Conversion 4→2
        cible.put(p.getX(), p.getY(), allume);   // Délégation
    }
}
```

C'est le **Design Pattern Adapter** : on adapte une interface à une autre sans modifier les deux extrémités.

---

**Q9 — Adaptateur24 : IDisplayBW → IDisplay**

Inverse d'Adaptateur42 : le pilote parle IDisplayBW, l'afficheur parle IDisplay.

```
[Pilote binaire (IDisplayBW)] ──IDisplayBW──> [Adaptateur24] ──IDisplay──> [TextSimulator]
```

Conversion : `true → Intensite(3)`, `false → Intensite(0)`

```java
class Adaptateur24 implements IDisplayBW {
    private IDisplay cible;

    Adaptateur24(IDisplay cible) { this.cible = cible; }

    @Override
    public void put(int x, int y, boolean allume) {
        Intensite i = allume ? new Intensite(3) : new Intensite(0);  // Conversion 2→4
        cible.put(new Point(x, y), i);
    }
}
```

**Remarque importante** : on perd de l'information dans Adaptateur42 (les niveaux 1 et 2 deviennent `true` comme le niveau 3). Adaptateur24 ne peut pas "inventer" des niveaux intermédiaires — c'est une limitation physique, pas un bug de code.

---

## Concepts clés du TP2

**Héritage (`extends`)** : une classe enfant réutilise le code de la classe parent.
`super()` appelle le constructeur parent, `super.methode()` appelle la méthode parent.
`@Override` demande au compilateur de vérifier qu'on redéfinit bien une méthode existante.

**Decorator** (Mirror) : on "enveloppe" un objet pour lui ajouter un comportement,
sans modifier l'objet enveloppé ni son utilisateur. Les deux voient toujours IDisplay.

**Adapter** (Adaptateur42, Adaptateur24) : on traduit une interface en une autre.
Permet de faire cohabiter du matériel ou des bibliothèques qui ne se connaissent pas.
