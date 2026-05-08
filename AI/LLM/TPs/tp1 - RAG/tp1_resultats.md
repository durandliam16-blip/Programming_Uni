Ici modèle + embedding (text --> Emb --> Vecteur), presque LLM (text --> Chat --> text)
Ici module emb diff de modèle emb
Modèle de langage complet = tok + emb + transformer + MLP

## Phase 1 : Installation

1. Telecharger .exe en lien et le lancer  
2. Dans terminal : ollama pull nomic-embed-text
3. Lancer fichier python  

Opés sur machine, cela implique de lancer deux composants :   
- le Serveur (Ollama) qui sera responsable du chargement des modèles neuronaux et de leur interrogation
- le Client (un script Python que vous créerez) chargé de la logique d'indexation, de recherche et d'interrogation

## Phase 2 : Vectorisation et Recherche

Pour RAG = indexer cette base documentaire afin de la rendre accessible au modèle via des requêtes. L'idée est de transformer chaque document en un vecteur numérique (embedding).  

### Étape 3 - Préparation de la base documentaire

**Embeddings : List[List[float]], en 2D cad 8 (nb_docs)*728 (taille_vecteurs)**

#### Question 1 - Génération des embeddings

**Implémentation de `generate_embeddings(docs)`:**
- Boucle sur chaque document de la base documentaire
- Appel à `get_embedding()` qui utilise l'API Ollama (modèle `nomic-embed-text`)
- Conversion de chaque embedding en numpy array float32 pour compatibilité avec FAISS
- Retourne une liste d'embeddings (vecteurs de dimension 384)

**Caractéristiques importantes:**
- Chaque embedding est un vecteur de **384 dimensions** (spécifique au modèle nomic-embed-text)
- Type de données: **float32** (optimisé pour FAISS et les calculs GPU)
- Les embeddings représentent la signification sémantique du texte
- Nécessite que le serveur Ollama soit actif et le modèle chargé

### Étape 4 - Indexation naïve par similarité cosinus

#### `cosine_similarity(v1, v2)`
Implémentation de la formule : (A · B) / (||A|| × ||B||)
- Calcul du produit scalaire
- Calcul des normes euclidiennes
- Gestion des cas limites (vecteurs nuls)
- Retourne une valeur entre -1 et 1

#### `naive_search(query, embeddings, docs, nb_results=3)`
Recherche exhaustive sur toute la base
- Vectorisation de la requête avec `get_embedding()`
- Calcul de la similarité cosinus avec chaque document
- Tri des résultats par score décroissant
- Retour des k meilleurs résultats

### Étape 5 - Indexation Industrielle avec FAISS

**Problème résolu:** La recherche naïve compare la requête avec TOUS les documents. Avec des millions de documents, c'est trop lent!

**Solution:** FAISS crée un index optimisé pour les recherches rapides (comme un index dans un livre).

#### `faiss_index(embeddings_np)`
Crée l'index FAISS
- Prend les embeddings de tous les documents
- Les normalise (L2 normalization selon tp)
- Les ajoute à un index FAISS
- Retourne l'index créé

#### `faiss_search(query, index, docs, nb_results=3)`
Recherche avec l'index
- Vectorise la requête
- Normalise le vecteur de la requête
- Cherche les k documents les plus proches dans l'index
- Retourne les résultats avec distances

**Gain de performance:** Au lieu de comparer avec N documents, FAISS utilise des structures de données optimisées pour chercher les plus proches voisins instantanément.

## Phase 3 : Génération Augmentée avec Gemma 3 (RAG)

Le RAG combine la **Récupération** de documents pertinents avec la **Génération** de réponses par un modèle LLM.

### Étape 6 - Interrogation de Gemma 3 avec le contexte

S'assure d'utiliser seulement le contexte qu'on lui donne sinon il doit dire qu'il ne sait pas. 
Grace à un prompt spécifique.

#### Concept du RAG

**Problème:** Un LLM standalone génère des réponses basées sur ses connaissances de pré-entraînement, qui peuvent être:
- Obsolètes
- Inexactes pour des domaines spécialisés
- Sans source

**Solution RAG:** 
1. Récupérer les documents pertinents (via FAISS)
2. Construire un **contexte** avec ces documents
3. Envoyer à Gemma 3 : "Réponds UNIQUEMENT avec ce contexte"
4. Le modèle génère une réponse basée sur les sources fiables

#### `rag_query(user_query, index, docs)`

**Avantage:** Les réponses sont basées sur la base documentaire, pas sur les hallucinations du modèle.

+ Q7 interface intercative à la fin du main

### Étape 7 (Bonus) - RAG Multimodal avec Gemma 3

Le RAG Multimodal ajoute la gestion **d'images** en plus du texte.


---

# 📚 RÉSUMÉ COMPLET POUR L'EXAMEN

## 1️⃣ CONCEPTS CLÉS

### Embedding (Vectorisation)
- **Définition:** Transformation d'un texte en vecteur de nombres (384 dimensions pour nomic-embed-text)
- **Utilité:** Permet de comparer sémantiquement deux textes via leur distance vectorielle
- **Obtention:** API Ollama → `client.embeddings(model="nomic-embed-text", prompt=text)`
- **Format:** numpy array float32 (optimisé pour calculs)

### Similarité Cosinus
- **Formule:** (A · B) / (||A|| × ||B||)
- **Résultat:** Valeur entre -1 (opposés) et 1 (identiques)
- **Cas limites:** Si l'un des vecteurs est nul → retourner 0.0
- **Complexité:** O(d) où d = dimension des embeddings

### Index FAISS
- **Objectif:** Accélérer la recherche de plus proches voisins (KNN)
- **Avantage:** O(k) au lieu de O(n×d)
- **Processus:** Normalisation L2 → IndexFlatL2 → Addition des vecteurs
- **Résultat:** Recherche instantanée même avec millions de documents

### RAG (Retrieval Augmented Generation)
- **Concept:** Récupération + Génération = Réponses fiables
- **Flux:** Requête → FAISS (trouve documents) → Contexte → Gemma 3 → Réponse
- **Avantage:** Les réponses sont basées sur des sources, pas hallucinations
- **Contrainte:** Prompt doit forcer "réponds UNIQUEMENT avec ce contexte"

### Pont Sémantique (Multimodal)
- **Idée:** Images et texte dans le MÊME espace vectoriel
- **Processus:** Image → base64 → Gemma 3 (description) → embedding
- **Résultat:** Recherche transversale (texte trouve images, et vice-versa)

---

## 2️⃣ FONCTIONS ESSENTIELLES

| Fonction | Entrée | Sortie | Rôle |
|----------|--------|--------|------|
| `get_embedding(text)` | Texte | Liste 384 nombres | Vectorise un texte |
| `generate_embeddings(docs)` | Liste textes | Liste embeddings | Vectorise plusieurs documents |
| `cosine_similarity(v1, v2)` | 2 vecteurs | Float [-1, 1] | Calcule similitude |
| `naive_search(query, embeddings, docs, k=3)` | Requête + docs | k-meilleurs résultats | Recherche exhaustive |
| `faiss_index(embeddings_np)` | Embeddings 2D | Index FAISS | Crée index optimisé |
| `faiss_search(query, index, docs, k=3)` | Requête + index | k-meilleurs résultats | Recherche rapide |
| `rag_query(query, index, docs)` | Requête + index | Réponse Gemma 3 | RAG simple |
| `generate_description_for_image(path)` | Chemin image | Description texte | Décrit image |
| `generate_multimodal_embeddings(docs)` | Docs mixtes | Embeddings mixtes | Vectorise texte+images |
| `multimodal_rag_query(query, index, docs)` | Requête + index | Réponse Gemma 3 | RAG multimodal |

---

## 4️⃣ CHIFFRES À RETENIR

| Paramètre | Valeur | Raison |
|-----------|--------|--------|
| Dimension embedding | 384 | Modèle nomic-embed-text |
| Type données | float32 | FAISS + GPU optimisé |
| Similarité cosinus range | [-1, 1] | Formule mathématique |
| Nombre résultats par défaut | 3 | Bon équilibre relevance/perf |
| L2 normalization | Avant IndexFlatL2 | Transforme cosinus en produit scalaire |

---

## 7️⃣ FLUX COMPLETS

### Flux Recherche Naïve
```
Texte requête
    ↓
get_embedding() → vecteur 384D
    ↓
Pour CHAQUE document:
  - get_embedding() → vecteur 384D
  - cosine_similarity(requête, doc)
    ↓
Trier par score décroissant
    ↓
Retourner top 3
```

### Flux Recherche FAISS
```
Embeddings documents
    ↓
faiss_index() → créer index optimisé
    ↓
Requête
    ↓
get_embedding() + normalisation
    ↓
index.search(requête, k=3)
    ↓
Retourner 3 documents + distances (instantané!)
```

### Flux RAG Complet
```
Requête utilisateur
    ↓
faiss_search() → récupérer contexte pertinent
    ↓
Construire prompt: "Contexte: {...}\nQuestion: {...}"
    ↓
client.chat(model="gemma3:4b", prompt)
    ↓
Afficher réponse Gemma 3
```

### Flux Multimodal
```
Documents (texte + images)
    ↓
Pour chaque image:
  - generate_description_for_image()
  - get_embedding(description)
    ↓
Pour chaque texte:
  - get_embedding(texte)
    ↓
Créer embeddings mixtes dans même espace 384D
    ↓
Recherche transpersonnelle (texte trouve images!)
```

---

## 9️⃣ COMMANDES IMPORTANTES

```bash
# Installation
pip install ollama numpy faiss-cpu

# Ollama - Terminal 1
ollama serve

# Ollama - Terminal 2
ollama pull nomic-embed-text

# Lancer le TP
python tp1_rag.py

# Tester un embedding
python -c "import ollama; print(ollama.embeddings(model='nomic-embed-text', prompt='test'))"
```
