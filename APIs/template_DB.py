# pip install sqlalchemy
# lancer dans terminal : uvicorn template_DB:app --reload

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

### Configuration de la connexion

# 1. On définit l'emplacement du fichier
SQLALCHEMY_DATABASE_URL = "sqlite:///./ma_base.db"
"""Anatomie de l'URL SQLite : l'URL suit toujours ce format : sqlite:///<chemin_vers_le_fichier>
- 3 barres (sqlite:///) : le chemin qui suit est relatif (par rapport au dossier où tu lances ton script)
- 4 barres (sqlite:////) : le chemin est absolu (depuis la racine)."""

# 2. On crée le moteur et la session
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

### Modèle de la table

class UserDB(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    email = Column(String, unique=True)

### Utiliser la DB

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware # pour lancer via HTML

# Cette ligne crée le fichier .db et les tables s'ils n'existent pas encore
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Autorise ton navigateur à accéder à l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En production, on remplace "*" par l'adresse du site
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fonction pour ouvrir/fermer la connexion à chaque requête
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/utilisateurs")
def creer_dans_db(nom: str, email: str, db: Session = Depends(get_db)):
    # 1. Créer l'objet
    nouvel_utilisateur = UserDB(nom=nom, email=email)
    # 2. L'ajouter à la session
    db.add(nouvel_utilisateur)
    # 3. Sauvegarder dans le fichier
    db.commit()
    return {"status": "Sauvegardé en base de données !"}

# --- LIRE (Accéder aux données) ---
@app.get("/utilisateurs")
def lire_utilisateurs(db: Session = Depends(get_db)):
    # .query(UserDB) demande à SQLAlchemy de récupérer tous les utilisateurs
    return db.query(UserDB).all()

# --- MODIFIER (Mettre à jour) ---
@app.put("/utilisateurs/{user_id}")
def modifier_utilisateur(user_id: int, nom: str, email: str, db: Session = Depends(get_db)):
    # 1. Chercher l'utilisateur
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        return {"error": "Utilisateur non trouvé"}
    
    # 2. Modifier les champs
    db_user.nom = nom
    db_user.email = email
    
    # 3. Sauvegarder
    db.commit()
    return {"status": "Utilisateur mis à jour", "data": {"nom": nom, "email": email}}

# --- SUPPRIMER ---
# L'ID est passé dans l'URL (ex: /utilisateurs/1)
@app.delete("/utilisateurs/{user_id}") 
def supprimer_utilisateur(user_id: int, db: Session = Depends(get_db)):
    # On cherche l'utilisateur qui a cet ID précis
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user:
        db.delete(user) # On le retire de la session
        db.commit()     # On valide la suppression dans le fichier .db
        return {"message": "Supprimé"}
    return {"error": "Non trouvé"}
