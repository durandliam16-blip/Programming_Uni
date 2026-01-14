# pip install requests

import requests

# 1. L'adresse de l'API (Endpoint)
url = "https://jsonplaceholder.typicode.com/posts/1"

# 2. On envoie la requête GET
reponse = requests.get(url)

# 3. On vérifie si ça a marché (Code 200)
if reponse.status_code == 200:
    # 4. On transforme le JSON reçu en dictionnaire Python
    donnees = reponse.json()
    print(f"Titre de l'article : {donnees['title']}")
else:
    print(f"Erreur : {reponse.status_code}")