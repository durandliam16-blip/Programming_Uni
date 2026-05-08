
Ce projet vise à simplifier la manipulation d'expressions mathématiques en Java. Plutôt que d'emboîter manuellement des constructeurs, nous implémentons un chaînage de méthodes permettant d'écrire du code qui ressemble presque à une formule mathématique naturelle.


## Étapes de conception

### 1. Base de l'Arbre (Modélisation)
Nous commençons par une classe abstraite `Expression` qui définit le contrat : chaque nœud de l'arbre doit être capable de s'évaluer en un `double`. Les classes `Entier` et `Reel` servent de "feuilles" (valeurs terminales).

### 2. Composition Récursive
La classe `Addition` (et plus tard `Multiplication`) représente un nœud interne. Elle ne contient pas de valeur, mais deux autres `Expression`. L'appel à `eval()` déclenche une cascade d'évaluations dans tout l'arbre jusqu'aux feuilles.

### 3. Mise en place de la Fluid API (Surcharge)
C'est le cœur du TP. Pour éviter d'écrire `new Addition(e1, e2)`, nous ajoutons les méthodes `add()` et `mul()` directement dans la classe `Expression`. 
* **Astuce technique :** Pour éviter la duplication de code, les méthodes acceptant un `int` ou un `double` créent simplement un nouvel objet (`Entier` ou `Reel`) et appellent la méthode `add(Expression)`.

### 4. Avantages de cette approche
* **Encapsulation :** L'utilisateur n'a plus besoin de manipuler explicitement les classes `Addition` ou `Multiplication`.
* **Lisibilité :** On passe de `new Addition(new Entier(2), new Entier(3))` à `new Entier(2).add(3)`.
* **Maintenabilité :** La logique de création des nœuds est centralisée.