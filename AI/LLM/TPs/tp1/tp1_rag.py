import time
import ollama
import numpy as np
import faiss
import sys
import os

os.environ['NO_PROXY'] = 'localhost,127.0.0.1,::1'

client = ollama.Client(host = 'http://127.0.0.1:11434')

# --- CONFIGURATION ---
# Modèle pour comprendre le sens du texte (Embeddings)
EMBED_MODEL = "nomic-embed-text" 
# Modèle pour générer la réponse (Chat)
CHAT_MODEL = "gemma3:4b" 

# ==============================================================================
# PHASE 2 : Vectorisation d'une base documentaire
# ==============================================================================

# ------------------------------------------------------------------------------
# Étape 3 : Préparation de la base documentaire

def get_embedding(text):
    """Génère le vecteur d'un texte via l'API Ollama."""
    try:
        response = client.embeddings(model=EMBED_MODEL, prompt=text)
        return response['embedding']
    except Exception as e:
        print(f"Erreur Ollama (vérifiez que 'ollama serve' tourne et que le modèle {EMBED_MODEL} est installé) : {e}")
        sys.exit(1)


def generate_embeddings(docs):
    """Génère les embeddings pour une liste de documents."""
    embeddings = []
    for doc in docs:
        embedding = get_embedding(doc)
        embeddings.append(np.array(embedding, dtype='float32'))
    return embeddings


# ------------------------------------------------------------------------------
# Étape 4 : Indexation naïve par similarité cosinus

#Q2
def cosine_similarity(v1, v2):
    """
    Calcule la similarité cosinus manuellement.
    Formule : (A . B) / (||A|| * ||B||)
    Retourne une valeur entre -1 (opposés) et 1 (identiques).
    """
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    
    cosine_sim = dot_product / (norm_v1 * norm_v2)
    return cosine_sim

#Q3
def naive_search(query : str, embeddings, docs, nb_results=3):
    """Recherche naïve par similarité cosinus."""
    # Les résultats seront des tuples (score, document)
    results = []
    query_embedding = get_embedding(query)
    
    for i, doc in enumerate(docs):
        similarity = cosine_similarity(query_embedding, embeddings[i])
        results.append((similarity, doc))
    
    # Trier par score décroissant et garder les meilleurs résultats
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:nb_results]


# ------------------------------------------------------------------------------
# Étape 5 : Indexation Industrielle avec Faiss

#Q4
def faiss_index(embeddings_np):
    """Crée un index FAISS à partir des embeddings."""
    # Ensure embeddings_np is 2D
    if embeddings_np.ndim == 1:
        embeddings_np = embeddings_np.reshape(1, -1)
    
    # Normaliser les vecteurs pour utiliser la similarité cosinus (produit scalaire sur vecteurs normalisés)
    embeddings_normalized = embeddings_np.astype(np.float32).copy()
    faiss.normalize_L2(embeddings_normalized)
    
    # Créer un index FAISS avec la métrique L2 (équivalent à cosinus pour vecteurs normalisés)
    dimension = embeddings_normalized.shape[1]
    index = faiss.IndexFlatL2(dimension)
    
    # Ajouter les vecteurs à l'index
    index.add(embeddings_normalized)
    
    return index

#Q5
def faiss_search(query, index, docs, nb_results=3):
    """Recherche avec Faiss."""
    # Les résultats seront des tuples (distance, document)
    results = []
    
    # Vectoriser la requête
    query_embedding = get_embedding(query)
    query_embedding = np.array([query_embedding], dtype='float32')
    
    # Normaliser le vecteur de requête
    faiss.normalize_L2(query_embedding)
    
    # Effectuer la recherche dans l'index
    distances, indices = index.search(query_embedding, nb_results)
    
    # Récupérer les documents correspondants
    for i, idx in enumerate(indices[0]):
        distance = distances[0][i]
        doc = docs[idx]
        results.append((distance, doc))
    
    return results


# ==============================================================================
# Phase 3 : Génération Augmentée avec Gemma 3
# ==============================================================================

# ------------------------------------------------------------------------------
# Étape 6 : Interrogation de Gemma 3 avec le contexte

def rag_query(user_query, index, docs):
    """Interroge Gemma 3 avec le contexte récupéré."""
    # Récupération du contexte via Faiss
    relevant_docs = faiss_search(user_query, index, docs, nb_results=3)
    
    # Construire le contexte à partir des documents pertinents
    context = "\n".join([f"- {doc}" for _, doc in relevant_docs])
    
    # Générer le prompt avec contexte
    system_prompt = f"""Tu es un assistant technique pour la machine Turbo-Encabulator 3000.
Un utilisateur pose une question. Réponds en utilisant UNIQUEMENT les informations du contexte fourni.
Si la réponse n'est pas dans le contexte, dis-le clairement.

Contexte (documents pertinents):
{context}

Question de l'utilisateur: {user_query}
Réponse:"""

    try:
        response = client.chat(
            model=CHAT_MODEL, 
            messages=[{'role': 'user', 'content': system_prompt}]
        )
        print("*** RÉPONSE DE GEMMA 3 ***")
        print("-" * 40)
        print(response['message']['content'])
        print("-" * 40)

    except Exception as e:
        print(f"Erreur lors de l'appel à Gemma : {e}")

#Q7 - Interface voir fin main


# ==============================================================================
# PHASE 3 : Bonus - RAG Multimodal avec Gemma 3
# ==============================================================================

# ------------------------------------------------------------------------------
# Étape 7 : Le Concept : Le "Pont Sémantique"

def generate_description_for_image(image_path):
    """Utilise Gemma 3 pour décrire une image."""
    import base64
    try:
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        response = client.chat(
            model=CHAT_MODEL,
            messages=[{
                'role': 'user',
                'content': 'Décris cette image en détail (machine Turbo-Encabulator)',
                'images': [image_data]
            }]
        )
        return response['message']['content']
    except FileNotFoundError:
        return f"Image: {image_path}"
    except Exception as e:
        print(f"Erreur lors de la génération de description: {e}")
        return ""

def generate_multimodal_embeddings(docs):
    """Génère les embeddings pour une liste de documents (texte + images)."""
    embeddings = []
    for doc in docs:
        if doc.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            description = generate_description_for_image(doc)
            embedding = get_embedding(description)
        else:
            embedding = get_embedding(doc)
        embeddings.append(np.array(embedding, dtype='float32'))
    return embeddings


def multimodal_rag_query(user_query, index, docs):
    """Interroge Gemma 3 avec le contexte multimodal récupéré."""
    relevant_docs = faiss_search(user_query, index, docs, nb_results=3)
    
    context_parts = []
    for _, doc in relevant_docs:
        if doc.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            context_parts.append(f"- [IMAGE] {doc}")
        else:
            context_parts.append(f"- {doc}")
    
    context = "\n".join(context_parts)
    
    system_prompt = f"""Tu es un assistant technique expert pour la machine Turbo-Encabulator 3000.
Tu dois répondre aux questions en utilisant le contexte fourni (texte et images).

Contexte (documents et images pertinentes):
{context}

Question de l'utilisateur: {user_query}
Réponse détaillée basée sur le contexte multimodal:"""
    
    try:
        response = client.chat(
            model=CHAT_MODEL,
            messages=[{'role': 'user', 'content': system_prompt}]
        )
        print("*** RÉPONSE MULTIMODALE DE GEMMA 3 ***")
        print("-" * 40)
        print(response['message']['content'])
        print("-" * 40)
    except Exception as e:
        print(f"Erreur lors de l'appel multimodal à Gemma : {e}")


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    # --- DONNÉES SIMULÉES (Documentation Technique) ---
    knowledge_base = [
        "La Turbo-Encabulator 3000 utilise un stator logarithmique pré-activé.",
        "Pour redémarrer le système d'urgence, maintenez le bouton rouge pendant 5 secondes, puis tournez la clé bleue.",
        "L'erreur 404 sur cette machine indique une surchauffe du condensateur fluxionnel principal.",
        "La maintenance des roulements à billes doit être effectuée tous les 150 cycles par un technicien certifié de niveau 2.",
        "Le voltage nominal d'entrée est de 220V, mais l'appareil tolère des fluctuations entre 210V et 240V.",
        "En cas de fuite de liquide réfrigérant (couleur verte), évacuez la zone immédiatement.",
        "Le module Wi-Fi se connecte uniquement sur la bande 2.4GHz avec le protocole WPA2.",
        "L'interface tactile peut se bloquer si l'opérateur porte des gants en latex non conducteurs."
    ]


    # Génération des embeddings
    print("\n--- Génération des embeddings pour la base documentaire ---")
    start_time_vectorisation = time.time()
    embeddings = generate_embeddings(knowledge_base)
    print(f"\t-> Embeddings générés pour {len(embeddings)} documents.")

    print(f"\t-> Conversion des embeddings en tableau numpy...")
    embeddings_np = np.array(embeddings)
    end_time_vectorisation = time.time()

    print(f"\t-> Taille du tableau numpy : {embeddings_np.shape}")
    print(f"\t-> Dimension des embeddings : {embeddings_np.shape[1]}")


    user_query = "Comment redémarrer la machine en cas d'urgence ?"

    # Indexation naïve
    print(f"\n--- Recherche naïve pour la question : '{user_query}' ---")
    start_time_manual_search = time.time()
    manual_results = naive_search(user_query, embeddings_np, knowledge_base, 3)
    end_time_manual_search = time.time()

    print(f"\t-> Résultats de la recherche naïve :")
    for score, doc in manual_results:
        print(f"\t   [Score: {score:.4f}] {doc}")


    # Indexation avec Faiss
    print(f"\n--- Création de l'index Faiss ---")
    start_time_faiss_index = time.time()
    index = faiss_index(embeddings_np)
    end_time_faiss_index = time.time()


    # Recherche avec Faiss
    print(f"\n--- Recherche optimisée avec FAISS pour la question : '{user_query}' ---")
    start_time_faiss_search = time.time()
    faiss_results = faiss_search(user_query, index, knowledge_base, 3)
    end_time_faiss_search = time.time()

    print(f"\t-> Résultats de la recherche FAISS :")
    for dist, doc in faiss_results:
        print(f"\t   [Distance: {dist:.4f}] {doc}")


    # Intégration du RAG avec Gemma 3
    print(f"\n--- Intégration RAG avec Gemma 3 pour la question : '{user_query}' ---")
    start_time_rag = time.time()
    rag_query(user_query, index, knowledge_base)
    end_time_rag = time.time()


    # RAG Multimodal avec Gemma 3 (Bonus)
    print(f"\n--- RAG Multimodal avec Gemma 3 (Bonus) ---")
    knowledge_base.append("images/turbo-encabulator_3000.png")
    # Génération des embeddings pour la nouvelle entrée (texte + image)
    print("-> Génération des embeddings multimodaux pour la base documentaire...")
    start_time_multimodal_vectorisation = time.time()
    multimodal_embeddings = generate_multimodal_embeddings(knowledge_base)
    end_time_multimodal_vectorisation = time.time()
    # Création de l'index Faiss multimodal
    print("-> Création de l'index Faiss multimodal...")
    start_time_multimodal_faiss_index = time.time()
    multimodal_index = faiss_index(np.array(multimodal_embeddings))
    end_time_multimodal_faiss_index = time.time()
    # Requête multimodale
    print("-> Requête multimodale...")
    start_time_multimodal_rag = time.time()
    multimodal_rag_query("Décris le fonctionnement de la Turbo-Encabulator 3000.", multimodal_index, knowledge_base)
    end_time_multimodal_rag = time.time()

    # Résumé des temps d'exécution
    print(f"\n\n####################################################\nRésumé des temps d'exécution :")
    print(f" - Vectorisation des documents : {end_time_vectorisation - start_time_vectorisation:.2f} secondes")
    print(f" - Recherche naïve : {end_time_manual_search - start_time_manual_search:.2f} secondes")
    print(f" - Création de l'index FAISS : {end_time_faiss_index - start_time_faiss_index:.2f} secondes")
    print(f" - Recherche FAISS : {end_time_faiss_search - start_time_faiss_search:.2f} secondes")
    print(f" - RAG avec Gemma 3 : {end_time_rag - start_time_rag:.2f} secondes")
    print("### Mode Multimodal ###")
    print(f" - Vectorisation Multimodale : {end_time_multimodal_vectorisation - start_time_multimodal_vectorisation:.2f} secondes")
    print(f" - Création de l'index FAISS Multimodal : {end_time_multimodal_faiss_index - start_time_multimodal_faiss_index:.2f} secondes")
    print(f" - RAG Multimodal avec Gemma 3 : {end_time_multimodal_rag - start_time_multimodal_rag:.2f} secondes")

    print(f"Dimension vecteur:{len(get_embedding('Test'))}") #verif de l'étape 3

    # ========== Q7 : INTERFACE UTILISATEUR INTERACTIVE ==========
    print("\n\n" + "="*60)
    print("INTERFACE UTILISATEUR INTERACTIVE - MOTEUR RAG")
    print("="*60)
    print("Vous pouvez maintenant poser des questions sur la Turbo-Encabulator 3000.")
    print("Tapez 'quitter' ou 'exit' pour terminer.\n")
    
    while True:
        try:
            # Récupérer la question de l'utilisateur
            user_input = input("\n📝 Votre question: ").strip()
            
            # Conditions de sortie
            if user_input.lower() in ['quitter', 'exit', 'q']:
                print("\n✅ Merci d'avoir utilisé le moteur RAG. Au revoir!")
                break
            
            # Vérifier que la question n'est pas vide
            if not user_input:
                print("⚠️  Veuillez poser une question non vide.")
                continue
            
            print(f"\n🔍 Traitement de votre question...\n")
            
            # Utiliser le moteur RAG
            rag_query(user_input, index, knowledge_base)
            
        except KeyboardInterrupt:
            print("\n\n✅ Interruption par l'utilisateur. Au revoir!")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")
            print("Veuillez réessayer avec une autre question.\n")
