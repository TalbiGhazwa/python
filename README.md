<h1 align="center">Reservation E_ticket</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/https://github.com/TalbiGhazwa/python?color=56BEB8">
  <img alt="Github language count" src="https://img.shields.io/github/languages/count/https://github.com/TalbiGhazwa/python?color=56BEB8">
  <img alt="Repository size" src="https://img.shields.io/github/repo-size/https://github.com/TalbiGhazwa/python?color=56BEB8">
  <img alt="License" src="https://img.shields.io/github/license/https://github.com/TalbiGhazwa/python?color=56BEB8">
</p>

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#gear-api-endpoints">API</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/TalbiGhazwa" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

Il s'agit d'un back-end développé avec **Flask** pour la gestion des événements et de la billetterie.

Fonctionnalités :
- Authentification basée sur JWT
- Accès différencié selon le rôle (administrateur / client)
- CRUD sur événements et catégories pour les admins
- Accès public aux événements disponibles

---

## :sparkles: Features ##

:heavy_check_mark: Authentification JWT ;  
:heavy_check_mark: Rôles utilisateurs (admin, client) ;  
:heavy_check_mark: CRUD événements pour admin ;  
:heavy_check_mark: CRUD catégories pour admin ;  
:heavy_check_mark: Accès public aux événements ;  
:heavy_check_mark: Intégration PostgreSQL ;  

---

## :gear: API Endpoints ##

### 🔐 Authentification

- **POST** `/api/inscription`  
  ➤ Créer un nouvel utilisateur (client par défaut)

- **POST** `/api/connexion`  
  ➤ Connexion d’un utilisateur et récupération du token JWT

---

### 👤 Utilisateur (admin)

- **GET** `/api/admin/clients`  
  ➤ Récupérer la liste des utilisateurs avec le rôle client  
  _(JWT requis, rôle: admin)_

---

### 📂 Catégories

- **GET** `/api/public/categori`  
  ➤ Obtenir la liste des catégories disponibles (accessible au public)

- **GET** `/api/categori/<id>`  
  ➤ Détails d'une catégorie spécifique  
  _(JWT requis, tous rôles)_

- **GET** `/api/admin/categori`  
  ➤ Lister toutes les catégories (admin uniquement)

- **POST** `/api/admin/categori`  
  ➤ Ajouter une nouvelle catégorie  
  _(JWT requis, rôle: admin)_

- **PUT** `/api/admin/categori/<id>`  
  ➤ Mettre à jour une catégorie spécifique  
  _(JWT requis, rôle: admin)_

- **DELETE** `/api/admin/categori/<id>`  
  ➤ Supprimer une catégorie  
  _(JWT requis, rôle: admin)_

---

### 🎫 Événements

- **GET** `/api/public/evenements`  
  ➤ Obtenir tous les événements disponibles publiquement

- **GET** `/api/public/evenements/<id>`  
  ➤ Détails d’un événement spécifique

- **(Autres endpoints CRUD pour admin peuvent être ajoutés si implémentés)**

---

## :rocket: Technologies ##

Ce projet utilise les technologies suivantes :

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/)
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [Render](https://render.com/)

---

## :white_check_mark: Requirements ##

- [GIT](https://git-scm.com)  
- [Python](https://www.python.org/)  
- [pip](https://pip.pypa.io/)  

---

## :checkered_flag: Starting ##

```bash
# Cloner le projet
git clone https://github.com/TalbiGhazwa/python

# Accéder au dossier du projet
cd python

# Créer et activer un environnement virtuel
python -m venv venv
source venv/bin/activate   # Sous Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le projet
python app.py

# Serveur accessible sur http://localhost:4200
