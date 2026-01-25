## I. Architecture et Fonctionnement Fondamental (Le "Cerveau" du LLM)

### 0. Géneration auto-agressive

C'est le processus par lequel un LLM produit du texte un jeton à la fois. À chaque étape, le modèle prédit le prochain jeton le plus probable, l'ajoute à la séquence d'entrée (contexte), puis utilise cette nouvelle séquence complète pour prédire le jeton suivant lors de l'itération suivante. Ce cycle se répète jusqu'à ce qu'un jeton de fin de texte soit généré.

### 1. Tokenisation : Le convertisseur langage-numérique 

* **Définition** : Découper un texte en groupes de caras et associer un jeton à chaque groupe afin de permettre au modèle de tariter le texte.

* **Processus** : Normalisation + Découpage en jetons (tokens)+ Encodage (transformation en entiers).

* **Méthode BPE (Byte-Pair Encoding)** : Découpe le texte en sous-mots pour gérer les mots inconnus et optimiser la taille du vocabulaire.

* **Limites** : Les jetons ne portent pas en eux la structure sémantique du langage naturel.

### 2. Embeddings (Plongements vectoriels) 

* **Embedding Initial** : Chaque jeton est transformé en un vecteur caractéristique de dimension n (ex: n=4096 pour Llama 3) dans un espace. À cette étape, le vecteur est **indépendant du contexte**.

* **Objectif** : Placer les concepts proches sémantiquement à une distance réduite dans l'espace multidimensionnel.

### 3. Mécanisme de Self-Attention (Auto-attention) 

* **Définition** : Calculer un nouveau vecteur caractéristique pour chaque jeton en tenant compte de l'ensemble du contexte de la phrase dans laquelle il apparait.

* **Fonctionnement technique** : Utilise des scores d'attention basés sur la similarité cosinus entre les vecteurs. Chaque jeton agit comme une **Query** (requête), une **Key** (clé) et une **Value** (valeur) pour mettre à jour sa représentation.

* **Complexité** : La complexité est de O(N**2) où N est le nombre de jetons, ce qui limite la fenêtre de contexte maximale.

### 4. Feed-Forward Network (FNN) 

* **Définition** : Réseau neuronal à propagation avant ajouté après l'attention pour augmenter la capacité du modèle.

* **Formule** : FNN(x) = ReLU(W*x+b)  
Avec W = Matrice de poids, b = Biais et ReLU = Fonction d'activation non-linéaire

### 5. Sortie et Stratégies de Génération 

* **Softmax & Température** : Le modèle produit une distribution de probabilités sur tout le vocabulaire. La température (T) ajuste cette distribution : une température basse favorise les jetons les plus probables, une température haute augmente la diversité (créativité).

* **Échantillonnage Glouton (Greedy Sampling)** : Choisir systématiquement le mot ayant la probabilité la plus élevée.

* **Détail** Après avoir transformé le texte d’entrée en jetons, puis calculé des représentations vectorielles à l’aide de l’embedding et du Transformer, le LLM ne génère pas directement un mot. En sortie, le modèle calcule une distribution de probabilités sur l’ensemble des jetons du vocabulaire. Chaque jeton possible se voit associer une probabilité correspondant à la probabilité d’être le prochain jeton, compte tenu du texte d’entrée et de son contexte. La génération du texte consiste ensuite à choisir un jeton à partir de cette distribution, en utilisant une stratégie de génération appropriée.

## II. Le Cycle de Vie : Du Modèle de Saisie à l'Assistant

### 1. Pré-entraînement (Initialisation) 

* **Données** : Textes bruts massifs issus d'Internet (Common Crawl, GitHub, Wikipedia).

* **Objectif** : Apprendre à prédire le prochain jeton (génération autorégressive).

* **Comportement** : Le modèle est un simple "moteur de saisie automatique" ; il ne sait pas encore suivre d'instructions.

* **Détails** : Lors de l’entraînement initial, un LLM est entraîné sur de très grandes qtés de textes provenant de sources variées. Ces données sont des textes bruts, sans instructions explicites et sans annotation spécifique destinée à un assistant. L’objectif principal de cet entraînement est d’apprendre à prédire le prochain jeton à partir du contexte fourni par les jetons précédents. En maximisant la probabilité du jeton suivant, le modèle apprend la structure du langage et les régularités linguistiques. À l’issue de cette phase, le modèle se comporte comme un moteur de saisie automatique.

* **A la fin** : Après l'entraînement initial sur de vastes corpus (Internet), le modèle se comporte comme un puissant moteur de saisie automatique. Bien qu'il possède de vastes connaissances, il ne sait pas suivre d'instructions : il cherche simplement à compléter statistiquement le texte commencé. Par exemple, si on lui pose une question, il pourrait continuer en écrivant une autre question similaire au lieu d'y répondre.

### 2. Post-entraînement (Alignement en 3 phases) 

* **Phase 1 : SFT (Supervised Fine-Tuning)** : Affinement sur des démonstrations de conversations "Utilisateur/Assistant" pour apprendre à répondre aux instructions.

* **Phase 2 : Modèle de Récompense** : Entraînement d'un second modèle pour simuler les préférences humaines en classant plusieurs réponses du LLM.

* **Phase 3 : RLHF (Reinforcement Learning from Human Feedback)** : Optimisation du LLM via l'apprentissage par renforcement pour maximiser la récompense définie en phase 2.

Renforcement = C'est le processus qui permet d'aligner le comportement du modèle sur les préférences humaines. Contrairement au pré-entraînement (qui prédit le mot suivant) ou au réglage supervisé (qui imite des exemples), l'apprentissage par renforcement apprend au modèle à maximiser une note de qualité (récompense).   

Lors de la troisième étape, appelée apprentissage par RLHF, le LLM et le modèle de récompense sont utilisés conjointement.
Le LLM génère des réponses à des requêtes, puis ces réponses sont évaluées par le modèle de récompense, qui attribue un score reflétant à quel point la réponse correspond aux préférences humaines (utilité, clarté, sécurité, etc.).
Le LLM est ensuite ajusté par apprentissage par renforcement de manière à maximiser la récompense fournie par le modèle de récompense.  Cette étape permet d’aligner le comportement du modèle avec les attentes des utilisateurs et de transformer un moteur de saisie automatique en un assistant plus utile et plus fiable.

_Le fonctionnement en 3 étapes (Processus RLHF) :_

* Création d'une base de préférences : On présente deux réponses générées par le LLM à un évaluateur humain. L'humain indique laquelle est la meilleure.

* Entraînement du Modèle de Récompense (Reward Model) : Un second modèle (plus petit) est entraîné à prédire le choix de l'humain. Il devient un "juge automatique" capable d'attribuer une note aux réps.

* Optimisation du LLM (La phase de Reinforcement) :
Le LLM génère une réponse + Le Modèle de Récompense note + Un algo d'optimisation (souvent PPO - Proximal Policy Optimization) met à jour les poids du LLM pour que les futures réponses obtiennent des notes plus élevées.

## III. Paradigmes d'Usage Avancés

### 1. RAG (Retrieval-Augmented Generation) 

* **Principe** : Enrichir le prompt avec des documents pertinents extraits d'une base de connaissances externe avant la génération.

* **Étapes** : Indexation (K-means clustering, FAISS)  Recherche des plus proches voisins (vecteurs)  Augmentation du contexte.

* **Avantages** : Réduit les **hallucinations** et contourne la **coupure de connaissances** (knowledge cutoff).

* **Détails** : 
1. Insuffisance sans RAG : Le modèle seul souffre de la coupure de connaissances (date limite d'entraînement) et n'a pas accès aux documents internes confidentiels ou très récents. 

2. Principe : Le RAG extrait des extraits pertinents d'une base de données externe via une recherche vectorielle et les injecte dans le contexte du prompt envoyé au LLM. 3. Réduction : En fournissant les sources directes au modèle, celui-ci peut s'appuyer sur des faits réels plutôt que sur sa mémoire imparfaite, limitant ainsi les inventions.

### 2. Agents IA et Approche ReAct

* **ReAct (Reasoning + Acting)** : Cycle en 4 étapes : **Pensée** (Reasoning)  **Action** (Appel d'outil)  **Observation** (Retour de l'outil)  **Réponse/Pensée suivante** (L'agent doit raisonner sur ce qu'il vient de voir (l'observation) pour décider de la suite ou conclure).

* **Système Prompt** : Crucial car il décrit les outils disponibles et les règles de raisonnement.  
Permet d'éviter d'entrainer un modèle pour chaque tache, réflechit tout .

* **Détails** : Dans une approche d’agent IA basée sur ReAct, le _system prompt_ joue un rôle central car il décrit l’environnement de l’agent et les actions possibles pour le LLM. C’est à travers le system prompt que le LLM comprend quelles fonctions sont disponibles, à quoi elles servent, et comment les appeler correctement (nom, paramètres). Lorsque le system prompt est clair et précis, le LLM peut raisonner correctement, choisir la bonne fonction et générer un appel exploitable par le système externe. Cela permet à l’agent de fonctionner de manière cohérente et fiable. À l’inverse, un system prompt imprécis ou ambigu peut entraîner des appels de fonctions incorrects, des paramètres erronés, ou des erreurs de parsing, ce qui réduit fortement la robustesse et l’efficacité de l’agent.

### 3. MCP (Model Context Protocol) 

* **Intérêt** : Standardiser l'interaction entre les agents et leur environnement (outils, bases de données) pour plus de robustesse et une découverte simplifiée des outils.

* **Détails** : 
1. Découverte : Permet à un agent de découvrir automatiquement les capacités et outils dispos dans son environnement de manière standardisée. 
2. Robustesse : En standardisant les formats d'échange entre l'IA et les applications tierces, il réduit les erreurs de compréhension et bugs.

### 4. Chain of thoughts

* 1. Intérêt : La chaîne de pensée permet au modèle de décomposer un problème complexe en étapes de raisonnement intermédiaires, ce qui améliore considérablement la précision sur des tâches mathématiques ou logiques.  

* 2. Entraînement : On peut entraîner un modèle soit par Few-shot prompting (fournir des exemples de raisonnement dans le prompt), soit par apprentissage par renforcement en récompensant le modèle lorsqu'il arrive au bon résultat final après un long raisonnement (comme pour DeepSeek-R1).

### Strats de géneration 

* 1. Différence : Les stratégies déterministes (comme le greedy sampling) choisissent toujours le jeton le plus probable, tandis que les stratégies basées sur la température ou le sampling introduisent du hasard pour augmenter la diversité. 
* 2. Avantages/Inconvénients : Greedy : Stable et rapide, mais risque de répétitions cycliques et manque de créativité. Sampling/Température : Plus naturel et créatif, mais peut produire des réponses incohérentes ou augmenter les hallucinations si la température est trop élevée.

## IV. Limites et Enjeux

* **Hallucinations** : Réponses plausibles mais factuellement fausses. Causes : Données d'entraînement contaminées, mémorisation imparfaite, ou stratégie de récompense en RLHF poussant le modèle à "deviner" pour plaire.

L'apprentissage par renforcement peut aggraver les hallucinations si le modèle de récompense valorise la forme de la réponse (ton sûr de soi) plutôt que la véracité, poussant l'IA à "deviner" ou inventer pour satisfaire l'utilisateur au lieu d'avouer son ignorance.

* **Impact Environnemental** : Consommation massive d'eau pour le refroidissement (jusqu'à 25,5M L/an pour 1MW) et fortes émissions de CO2 (ex: 1900 tonnes pour l'entraînement de certains modèles). + Elec pour alimenter les GPU

* **Éthique et Juridique** : Problèmes de droits d'auteur sur les données d'entraînement (procès contre Anthropic, OpenAI, etc.).