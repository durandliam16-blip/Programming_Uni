# pip install sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from .database import Base

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