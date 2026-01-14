from fastapi import FastAPI, HTTPException # Pour créer APIs
from pydantic import BaseModel # Pour biblio vérif
from typing import Optional # Pour notation

app = FastAPI()

# --- 1. Simulation de la base de données ---
db_utilisateurs = [
    {"id": 1, "nom": "Alice", "role": "Admin"},
    {"id": 2, "nom": "Bob", "role": "Utilisateur"}
]

# --- 2. Modèle de données ---
class Utilisateur(BaseModel):
    id: int
    nom: str
    role: str = "Utilisateur" # Valeur par défaut

# --- 3. Les Routes ---

# Récupérer tous les utilisateurs (GET)
@app.get("/utilisateurs") # pas {user_id} car veut génerale
def liste_utilisateurs():
    return db_utilisateurs

# Ajouter un utilisateur (POST)
@app.post("/utilisateurs/{user_id}")
def creer_utilisateur(nouvel_utilisateur: Utilisateur):
    # On transforme l'objet Pydantic en dictionnaire Python
    utilisateur_dict = nouvel_utilisateur.dict()
    # On l'ajoute à notre "base de données"
    db_utilisateurs.append(utilisateur_dict)
    return {"message": "Utilisateur ajouté !", "donnees": utilisateur_dict}

# Modifier un utilisateur (PUT)
@app.put("/utilisateurs/{user_id}")
def modifier_donnees(user_id: int, utilisateur_modifie: Utilisateur):
    # On cherche l'utilisateur dans notre liste
    for index, user in db_utilisateurs.items():
        if user["id"] == user_id:
            db_utilisateurs[index] = utilisateur_modifie.dict() # modif
            return {"message": "Utilisateur mis à jour", "donnees": db_utilisateurs[index]}
    # Si pas trouvé
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

# Supprimer un utilisateur (DELETE)
@app.delete("/utilisateurs/{user_id}")
def supprimer_utilisateur(user_id: int):
    # On cherche l'utilisateur dans notre liste
    for index, user in db_utilisateurs.items():
        if user["id"] == user_id:
            del db_utilisateurs[index] # supprime
            return {"message": f"L'utilisateur {user_id} a été supprimé"}
    # Si pas trouvé
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

# Ex fonctions différentes des 4 classiques
@app.get("/stats/roles")
def obtenir_stats_roles():
    # Calcule le nombre total d'utilisateurs par rôle
    admin_count = len([user for user in db_utilisateurs if user["role"] == "Admin"])
    return {"total": len(db_utilisateurs),
            "admins": admin_count,
            "utilisateurs_simples": len(db_utilisateurs) - admin_count}

# --- 4. Lancement auto ---

if __name__ == "__main__": 
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)