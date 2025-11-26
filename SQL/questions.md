# Modèle et langages relationnels 2024-2025

fichier `ratingdb-fr.md`

Soit une base de données de type IMDB, qui enregistre les évaluations de films par des utilisateurs (critiques amateurs). Le schéma de la base est le suivant :

```sql
Movie(mID, title, year_, director)
Reviewer(rID, name_)
Rating(rID, mID, stars, ratingDate)
```

## Partie A

Écrire chacune des requêtes suivantes en **SQL** puis les tester sur une instance de la base de données, disponible en anglais. Proposer plusieurs formulations s'il y a lieu. Commenter directement dans le script SQL.

### SQL conjonctif

Donner 2 versions pour chaque requête : SQL déclaratif et SQL procédural

1. Titre des films réalisés par _Steven Spielberg_.
2. Titre et réalisateur des films sortis entre 1980 et 2000, et réalisés soit par James Cameron, soit par Steven Spielberg.
3. Titre et réalisateur des films évalués le 22 janvier 2011.
4. Nom de l'évaluateur, note et date des évaluations du film "_Gone with the Wind_".
5. Couple de noms d'évaluateurs, sans répétition ((a,b) et (b,a) sont identiques, (a,a) inutile), qui ont notés les mêmes films.

### SQL relationnel

6. Nom des réalisateurs de films sortis avant 1980 ainsi que ceux des évaluateurs qui ont notés des films de _Steven Spielberg_.
7. Titre, réalisateur et année de sortie des films qui n'ont pas été évalués par _Chris Jackson_.
8. Nom des évaluateurs ayant mis la meilleure note (quelle qu'elle soit) des films de _Steven Spielberg_. Proposer une version avec le MAX, et une sans.
9. Nom des évaluateurs qui ont notés tous les films réalisés par _Steven Spielberg_. Proposer les 4 versions de la division.

## Partie B

Proposer une ou plusieurs expressions **SQL** pour les requêtes suivantes.

10. Titres de films, avec, si elle existe, la date de leur première évaluation.
11. Trouver le(s) film(s) ayant la meilleure note en moyenne.
12. Trouver la différence entre la moyenne des notes moyennes par film sortis avant 1980, et celle des films sortis après 1980. S'assurer de calculer d'abord la moyenne par film, puis d'en faire la moyenne globale pour chacune des deux périodes.
13. Pour chaque réalisateur, trouver le film qui a reçu la meilleure note. Présenter au résultat le nom du réalisateur, le titre du film et la note obtenue. En cas d'ex aequo, présenter tous les "meilleurs" films d'un même réalisateur. Ignorer les films dont le réalisateur est inconnu.

## Partie C

Proposer une formulation en SQL des requêtes de **mise-à-jour** suivantes.

14. Ajouter l'évaluateur Roger Ebert d'identifiant 209.
15. Insérer la note maximale de 5 donnée par James Cameron à tous les films de la base de données. Ne pas renseigner la date.
16. Pour tous les films qui ont une note moyenne de 4 ou plus, ajouter 25 ans à la date de sortie, en modifiant les nuplets existants.
17. Supprimer toutes les évaluations des films sortis avant 1970 ou après 2000, pour lesquels la note est inférieure à 4.

## Partie D

### D.1

Ajouter les **contraintes** suivantes au schéma de la base :

i. les clés primaires et clés étrangères, avec propagation en cas de modification
ii. l'unicité de Film(titre) et Évaluateur(nom)
iii. les attributs non nuls
iv. les contraintes de domaine sur Film(année) et Appréciation(note)
v. une contrainte de nuplet dans Appréciation.

Pour chacune des contraintes, proposer un (contre-)exemple qui montre son utilité.

### D.2

Proposer :

v. une assertion, si le système de gestion de base de données le permet
vi. un déclencheur
vii. une fonction personnalisée (User Defined Function)
viii. une procédure stockée

Pour chacun, proposer un micro-scénario qui montre son utilité.

## Partie E [Bonus]

Résoudre l'[énigme du crime SQL](https://mystery.knightlab.com/) ! Fournir les requêtes SQL successives, et documenter le raisonnement.
