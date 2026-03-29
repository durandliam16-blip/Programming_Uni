# TP n°1 — Programmation Orientée Objet en Java
## Encapsulation, Interfaces — INFO3/IDIA3 Polytech Nantes

---

## Structure des fichiers

```
tp1/
├── Hello.java            # Q1-2, Q9  — Point d'entrée du programme
├── Message.java          # Q4, Q9   — Classe utilisant une Langue
├── French.java           # Q6, Q8   — Implémentation concrète de Langue
├── Langue.java           # Q7       — Interface "contrat" pour les langues
│
├── IFifo.java            # Q10-11   — Interface file d'attente (FIFO)
├── IMemoire.java         # Q14      — Interface commune à toutes les puces
├── Memoire32.java        # Q12      — Simulation puce 32 Mo (fabricant 1)
├── Puce64.java           # Q14      — Simulation puce 64 Mo (fabricant 2)
│
├── Buffer32.java         # Q12      — Buffer FIFO utilisant Memoire32 (couplage fort)
├── BufferGen.java        # Q14-15   — Buffer FIFO générique via IMemoire (couplage faible)
├── MemoireDouble.java    # Q18      — Solution 1 : adaptateur deux puces → une IMemoire
├── BufferDeuxPuces.java  # Q18      — Solution 2 : buffer gérant deux puces directement
│
└── TestBuffer.java       # Q12      — Jeu de tests (35 tests, tous passés ✓)
```

---

## Commandes de compilation et d'exécution

```bash
# Compiler TOUS les fichiers en une fois
javac *.java

# Exécuter le programme principal (affiche "bonjour")
java Hello

# Exécuter les tests du buffer
java TestBuffer
```

> **Note :** `javac Hello.java` compile aussi les dépendances **directes** (Message, French),
> mais PAS les dépendances de dépendances (ex: si French dépend d'une autre classe).
> Pour éviter ce problème → utiliser `javac *.java` ou un outil de build (Maven, Gradle).

---

## Réponses aux questions

---

### Section 1 — Compiler et exécuter un programme Java

**Q1 & Q2 — Compilation et exécution de Hello**

```bash
javac Hello.java   # Produit Hello.class (bytecode)
java Hello         # Exécute la JVM sur la classe Hello → affiche "Hello"
```

Le compilateur (`javac`) transforme le code source `.java` en **bytecode** `.class`.
La JVM (`java`) interprète ce bytecode. Java est donc **partiellement compilé, partiellement interprété**.

---

**Q3 — Plusieurs compilateurs/JVM ?**

Pour vérifier les versions disponibles :
```bash
javac -version        # version du compilateur actif
java -version         # version de la JVM active
update-alternatives --list javac   # liste des compilateurs (Linux)
ls /usr/lib/jvm/      # liste des JDK installés
```

En environnement universitaire, il peut y avoir plusieurs JDK installés (ex: Java 11, Java 17, Java 21).
Chaque version peut compiler pour une version cible différente (`-source`, `-target`).

---

**Q4 — Compilation avec dépendances directes**

Quand on compile `Hello.java` qui utilise `Message` :
```bash
javac Hello.java
```
Java détecte que `Hello` dépend de `Message` et **recompile automatiquement `Message.java`**.

Fichiers `.class` créés : `Hello.class` **et** `Message.class`.

---

**Q5 — Modification de Message.java, recompilation avec javac Hello.java**

```bash
# Modifier Message.java (hello → HELLO)
javac Hello.java
java Hello           # Affiche : HELLO
```

`Message.java` **a bien été recompilé** car il est une dépendance directe de `Hello`.

---

**Q6 — Problème avec une indirection supplémentaire (Hello → Message → French)**

```bash
# Modifier French.java
javac Hello.java     # Compile Hello + Message, mais PAS French !
java Hello           # Affiche l'ANCIENNE valeur de French
```

**Constat :** `javac Hello.java` recompile les dépendances **directes** de Hello (= Message),
mais pas les dépendances de Message (= French).
La modification de `French.java` n'est pas prise en compte.

**Solution :** `javac *.java` pour tout recompiler, ou utiliser **Maven / Gradle**.

---

### Section 2 — Interfaces

**Q7 — Interface `Langue`**

```java
interface Langue {
    String hello();   // Contrat : toute Langue sait dire "hello" dans sa langue
}
```

Une interface = un **contrat** : liste de méthodes que toute classe implémentante DOIT fournir.
Pas de corps de méthode, pas d'état (pas de champs d'instance).

---

**Q8 — `French` conforme à l'interface `Langue`**

```java
class French implements Langue {
    @Override
    public String hello() {
        return "bonjour";
    }
}
```

Le mot-clé `implements Langue` oblige le compilateur à vérifier que `hello()` est présente.
Sans cette méthode → **erreur de compilation**.

---

**Q9 — Exploitation du sous-typage dans `Message` et `Hello`**

Principe : **programmer vers une interface, pas vers une implémentation**.

```java
// Message.java — le champ est de type Langue, pas French
class Message {
    private Langue langue;                  // interface, pas classe concrète
    Message(Langue langue) {               // injection de dépendance
        this.langue = langue;
    }
    void print() {
        System.out.println(langue.hello()); // polymorphisme
    }
}

// Hello.java — on peut changer de langue en modifiant UNE seule ligne
Langue maLangue = new French();  // ← seule cette ligne change si on veut Spanish, etc.
Message m = new Message(maLangue);
m.print();
```

**Avantage :** `Message` ne connaît plus `French`. Si on ajoute `Spanish`, `Message` ne change pas.

---

### Section 3 — Mémoire tampon (Buffer)

**Q10 — Méthodes minimales d'une file d'attente (FIFO)**

| Méthode | Rôle |
|---|---|
| `void enqueue(byte b)` | Ajouter un octet en fin de file |
| `byte dequeue()` | Retirer et retourner le plus vieil octet |
| `boolean isEmpty()` | Savoir si la file est vide |
| `boolean isFull()` | Savoir si la file est pleine |

---

**Q11 — Pourquoi une interface plutôt qu'une classe ?**

Si on code directement avec une classe :
- On est **lié** à cette implémentation concrète
- Si le fabricant change la puce, on doit modifier tout le code

Avec une **interface** :
- On code contre un **contrat stable** (`IFifo`)
- Le fabricant livre une nouvelle implémentation → on la branche sans rien changer
- On peut aussi créer une implémentation de **test** (tableau Java) indépendamment du hardware

---

**Q12 — Implémentation de `Buffer32` : buffer circulaire**

**Principe du buffer circulaire :**
```
Mémoire vue comme un anneau :
[0][1][2][3]...[readPtr]...[writePtr]...[33554431]
                  ^               ^
          prochain à lire   prochain à écrire

Quand writePtr atteint la fin → il revient à 0 (opération modulo)
```

**Gestion de la fin de puce (wrap-around) :**
```java
writePtr = (writePtr + 1) % TAILLE;  // modulo → retour à 0 automatiquement
readPtr  = (readPtr  + 1) % TAILLE;
```

**Distinguer "vide" et "plein" :** dans les deux cas `writePtr == readPtr` !
→ On utilise un **compteur** (`count`) pour lever l'ambiguïté.

**Jeu de tests :** voir `TestBuffer.java` (35 tests passés ✓)
```bash
java TestBuffer
# Affiche : 35 / 35 tests réussis.
```

---

**Q13 — Combien de lignes modifier pour une autre puce dans `Buffer32` ?**

**Toutes les occurrences du mot `Memoire32`** dans la classe :
- La déclaration du champ : `private Memoire32 puce;`
- Le type du paramètre du constructeur : `Buffer32(Memoire32 puce)`
- La constante de taille : `Memoire32.TAILLE`

→ **3+ occurrences** à modifier manuellement, risque d'oubli.

**Solution propre → Question 14 : utiliser `IMemoire`.**

---

**Q14 — `BufferGen` : buffer générique via `IMemoire`**

```java
class BufferGen implements IFifo {
    private IMemoire puce;   // ← IMemoire au lieu de Memoire32
    private int taille;

    BufferGen(IMemoire puce, int taille) {  // reçoit n'importe quelle IMemoire
        this.puce = puce;
        this.taille = taille;
        ...
    }
}
```

Test avec deux puces différentes :
```java
// Puce 32 Mo
BufferGen b1 = new BufferGen(new Memoire32(), Memoire32.TAILLE);

// Puce 64 Mo — SEULES ces deux lignes changent, BufferGen est identique
BufferGen b2 = new BufferGen(new Puce64(), Puce64.TAILLE);
```

---

**Q15 — Combien de lignes modifier dans `BufferGen` pour changer de puce ?**

**ZÉRO ligne** dans `BufferGen` lui-même.
On change uniquement la ligne qui instancie le buffer (dans le `main` ou le code client).

C'est la puissance des interfaces : **le code métier ne connaît pas le matériel**.

---

**Q16 & Q17 — Modularité : remplacer un `.class` sans recompiler**

```bash
# Sauvegarder sa propre implémentation
mkdir ../sauvegarde && cp BufferGen.java BufferGen.class ../sauvegarde/
rm BufferGen.java BufferGen.class

# Récupérer le .class d'un camarade (sans son .java)
# cp /chemin/camarade/BufferGen.class .

# Recompiler UNIQUEMENT la classe de test (pas besoin du .java de BufferGen)
javac TestBuffer.java   # utilise le .class de BufferGen déjà présent

# Lancer les tests sur l'implémentation du camarade
java TestBuffer
```

**Q17 — Propriété de la modularité :**
> On peut **remplacer un module compilé** (`.class`) sans recompiler les modules qui l'utilisent,
> tant que l'**interface** (contrat) reste identique.
> Chaque équipe peut développer, tester et livrer son module indépendamment.
> C'est le fondement du travail en équipe sur les grands projets.

---

**Q18 — Deux solutions pour deux puces**

### Solution 1 : Adaptateur `MemoireDouble` (recommandée ✓)

```
[BufferGen] → voit un seul IMemoire
                    ↓
             [MemoireDouble]  ← adaptateur
              /            \
        [Puce A]          [Puce B]
```

```java
int moitie = 16 * 1024 * 1024;  // 16 Mo chacune
IMemoire double32 = new MemoireDouble(new Memoire32(), new Memoire32(), moitie);
BufferGen buf = new BufferGen(double32, moitie * 2);
```

**Avantage :** `BufferGen` ne change **absolument pas**.
La logique de bascule entre puces est encapsulée dans `MemoireDouble`.

### Solution 2 : `BufferDeuxPuces` (gestion interne)

```java
BufferDeuxPuces buf = new BufferDeuxPuces(
    new Memoire32(), Memoire32.TAILLE,
    new Puce64(),    Puce64.TAILLE
);
```

**Inconvénient :** La logique de bascule est dans le buffer lui-même → **moins modulaire**.
Si on veut 3 puces demain, il faut réécrire `BufferDeuxPuces`.

**Comparaison :**

| Critère | Solution 1 (MemoireDouble) | Solution 2 (BufferDeuxPuces) |
|---|---|---|
| Modification de BufferGen | Aucune | N/A (nouvelle classe) |
| Facilité d'extension (3 puces) | Facile (MemoireTriple) | Difficile (réécrire) |
| Séparation des responsabilités | ✓ Bonne | ✗ Mélangée |
| Lisibilité | ✓ Claire | Acceptable |

---

## Concepts clés à retenir

**Encapsulation** — Cacher les détails d'implémentation derrière une interface.
Le code client ne sait pas *comment* c'est fait, seulement *quoi* ça fait.

**Interface** — Contrat entre un fournisseur et un utilisateur.
Permet de changer l'implémentation sans modifier le code client.

**Sous-typage / Polymorphisme** — Un objet `French` peut être utilisé partout où un `Langue` est attendu.
Le comportement réel (la méthode appelée) dépend du **type réel** de l'objet, pas du type déclaré.

**Injection de dépendance** — Passer les dépendances en paramètre du constructeur plutôt que de les créer à l'intérieur.
Rend le code plus testable et plus flexible.

**Modularité** — Chaque classe a une responsabilité claire et peut être remplacée indépendamment.
