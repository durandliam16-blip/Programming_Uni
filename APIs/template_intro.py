### INSTANCIATION

#pip install fastapi uvicorn
from fastapi import FastAPI

# 1. On crée l'instance de l'API
app = FastAPI()

# 2. On définit une route (Endpoint)
#Si qqn arrive sur l'adresse racine (/) avec GET, exécute la fonction en dessous"""
@app.get("/")
def message_accueil():
    return {"message": "Bienvenue sur mon API !"}

# 3. Une autre route avec un paramètre
@app.get("/saluer/{nom}")
def saluer_utilisateur(nom: str):
    return {"message": f"Bonjour {nom}, comment vas-tu ?"} #Transforme dico en python

### LANCER

# 1. Lancer fichier
# 2. Terminal : uvicorn main:app --reload
# ou remplacer automatiquement par : 
if __name__ == "__main__": 
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# 3. Documentation : http://127.0.0.1:8000/docs 
# 4. Ouvre adresse http://127.0.0.1:8000 puis http://127.0.0.1:8000/saluer/Lucas 
