# 🎬 Movie Viewer

Movie Viewer est une application web développée avec **Flask** qui permet de rechercher des films via l’API [OMDb](https://www.omdbapi.com/), d’afficher leurs détails, et de gérer les utilisateurs avec un système d’authentification (inscription / connexion / rôle admin).


## 🚀 Fonctionnalités

-   🔎 **Recherche de films** par titre via l’API OMDb.
-   📖 **Affichage des détails** d’un film (titre, résumé, année, acteurs, affiche, etc.).
-   👤 **Authentification des utilisateurs** :
    -   Inscription / Connexion / Déconnexion.
    -   Gestion de session sécurisée.
-   🛠️ **Espace Admin** :
    -   Tableau de bord pour la gestion des utilisateurs (ajout, suppression, modification des rôles).
-   🖥️ **Interface simple** et responsive pour une expérience utilisateur optimale.

---

## 📂 Structure du projet
```bash
    movie_viewer/
        │── app.py # Point d’entrée Flask
        │── config.py # Configuration générale
        │── models.py # Modèles (User, etc.)
        │── forms.py # Formulaires (login/register)
        │── requirements.txt # Dépendances Python
        │── static/ # Fichiers statiques (CSS, JS, images)
        │── templates/ # Templates HTML (Jinja2)
        │── instance/ # Base SQLite (créée automatiquement)
        └── README.md # Ce fichier
```
---

## ⚙️ Installation et utilisation

### 1️⃣ Cloner le projet
```bash
    git clone https://github.com/AdamFARTOUT/movie_viewer.git
    cd movie_viewer
```
### 2️⃣ Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```
### 3️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```
### 4️⃣Lancer l’application
```bash
python -u app.py
```

## 🛠️ Technologies utilisées

    Backend : Flask (Python)

    Base de données : SQLite

    Templates : Jinja2

    Formulaires : Flask-WTF

    Sécurité : Flask-Login + Werkzeug

    API externe : OMDb API
    
## 👨‍💻 Auteur

Projet développé par Adam Fartout