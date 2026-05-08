## Clonage et Sérialisation de Graphes Routiers

Ce projet implémente une structure de données pour la navigation routière, permettant la recherche d'itinéraires, la copie profonde de cartes et la sauvegarde via sérialisation.

### 1. Structure de données (Questions 1 à 5)

* **Q1. Algorithme de plus court chemin :** Pour l'algorithme de Dijkstra, on utilise généralement une **liste d'adjacence** combinée à une file de priorité (*PriorityQueue*).
* **Q2. Architectures proposées :** 
    * **Architecture A (Orientée Objet Pure) :** Une classe `City` contenant une liste d'objets `Edge`. L'objet `Edge` contient une référence vers la `City` de destination et un poids.
    * **Architecture B (Basée sur les Collections) :** Une classe `RoadMap` utilisant une `Map<String, Map<String, Double>>` où la clé est le nom de la ville de départ et la valeur est un dictionnaire des destinations avec leurs distances.
* **Q3. Représentation d'un chemin :** Un chemin est représenté par une `List<City>` ou une `List<String>`, ordonnée du départ à l'arrivée. 
* **Q4. Avantages et inconvénients :** 
    * **Architecture A :** Plus intuitive et facile à étendre (on peut ajouter des attributs aux villes), mais plus complexe à cloner à cause des références cycliques.
    * **Architecture B :** Très rapide pour les accès directs et simple à sérialiser, mais moins "objet" et moins flexible si la complexité des données augmente.
* **Q5. Choix :** Nous choisissons l'**Architecture A** car elle permet de mieux illustrer les problématiques de clonage profond et de sérialisation d'objets interconnectés.

---

### 2. Implémentation technique

#### Étapes de réalisation :
1. **Définition des classes :** Création de `City` et `Edge` implémentant `Serializable` et `Cloneable`. 
2. **Affichage :** Redéfinition de `toString()` pour visualiser le graphe (ex: "Nantes -> [Angers (0.95), Poitiers (2.1)]"). 
3. **Initialisation :** Création du graphe incluant les 10 villes (Rouen, Paris, Le Mans, Rennes, Brest, Angers, Tours, Nantes, Poitiers) et leurs 12 connexions.


---

### 3. Copie et Égalité (Questions 8 à 12)

* **Q8. Type de copie :** Une **copie profonde** est nécessaire. Si l'on effectue une copie superficielle, modifier l'état "visité" d'une ville dans la copie modifierait aussi l'original, rendant l'algorithme instable.
* **Q9. Immutabilité :** Comme `String` et `Integer` sont immutables en Java, il n'est pas nécessaire de les cloner explicitement à l'intérieur des objets ; copier la référence suffit pour ces types.
* **Q11. Égalité par `==` vs `equals` :**
    * `carte1 == carte2` sera **false** car ce sont deux instances distinctes en mémoire.
    * `carte1.equals(carte2)` sera **true** si la méthode est correctement redéfinie pour comparer le contenu (noms des villes et structure des voisins).

---

### 4. Sérialisation (Questions 14 à 18)

* **Mécanisme :** Utilisation de `ObjectOutputStream` pour l'écriture et `ObjectInputStream` pour la lecture.
* **Q18. Post-désérialisation :**
    * `==` reste **false** : l'objet reconstruit est une nouvelle instance.
    * `equals()` est **true** : les données reconstruites sont identiques à l'original.

---

### Code Source

Voir code.

### Instructions de test
* Lancez la classe `Main`.
* Le programme génère un fichier `map.ser`.
* Il compare ensuite le chemin trouvé avant et après la restauration du fichier.