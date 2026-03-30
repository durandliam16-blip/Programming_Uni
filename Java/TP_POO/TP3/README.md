> Ce projet implémente une liste chaînée en utilisant le polymorphisme dynamique pour remplacer les vérifications explicites de nullité par une structure d'objets.

## 📋 Étapes de réalisation
Définition de l'abstraction : Création de l'interface Liste définissant le contrat (méthodes communes).

Gestion du cas vide : Création de la classe Vide. Contrairement au C, la liste vide est ici un objet réel, ce qui évite les NullPointerException. 


Gestion des maillons : Création de la classe Cellule qui contient une valeur et une référence vers la suite de la liste (de type Liste). 


Implémentation récursive : Chaque méthode est implémentée de manière récursive sans aucune structure de contrôle if (c == null). 

## ❓ Réponses aux Questions

### Question 3 : toString par défaut dans une interface ? 

Non, il est impossible de définir toString() comme méthode default dans une interface.

En Java, les méthodes de la classe Object (comme toString, equals, hashCode) ont toujours la priorité sur les implémentations par défaut des interfaces. Une interface ne peut pas "gagner" contre la hiérarchie de la classe Object.

### Question 4 : Documentation et Surcharge de print 

Documentation : La méthode System.out.print appartient à la classe java.io.PrintStream.

Surcharge : Oui, la méthode est fortement surchargée (print(String), print(int), print(Object), print(boolean), etc.). 

Résultat de print(Object) : Lorsqu'on utilise print(Object), Java appelle en interne String.valueOf(obj), qui lui-même appelle obj.toString(). Le résultat affiché est donc bien celui défini dans notre méthode toString() redéfinie. 

### Question 5 à 9 : Listes dans la plateforme Java 

Documentation : L'interface List se trouve dans java.util.List. 

Hiérarchie (Question 9) : Les méthodes isEmpty(), size() et contains() sont également déclarées dans les super-interfaces : 

Collection : L'interface parente directe de List.

Iterable : L'interface racine pour toutes les collections pouvant être parcourues.