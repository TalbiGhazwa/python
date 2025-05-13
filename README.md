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

## Points d'Entrée de l'API

### URL de Base

`http://127.0.0.1:5000/api/`

### Endpoints

1. **Inscription utilisateur**
   - **POST** `/api/inscription`
   - Corps de la Requête :
     ```json
    {
  "nomUtilisateur": "Ali",
  "prenomUtilisateur": "Ben Salah",
  "email": "ali@example.com",
  "motPasse": "123456",
  "role": "CLIENT"
  }

     ```
   - Réponse :
     ```json
      {
  "message": "Utilisateur inscrit avec succès"
  }

     ```

2. **Récupérer Tous les Films**
   - **GET** `/`
   - Réponse :
     ```json
     [
       {
         "id": 1,
         "title": "Inception",
         "director": "Christopher Nolan",
         "year": 2010,
         "genre": "Science Fiction"
       }
     ]
     ```

3. **Récupérer un Film par ID**
   - **GET** `/{movie_id}`
   - Réponse :
     ```json
     {
       "id": 1,
       "title": "Inception",
       "director": "Christopher Nolan",
       "year": 2010,
       "genre": "Science Fiction"
     }
     ```

4. **Mettre à Jour un Film**
   - **PUT** `/{movie_id}`
   - Corps de la Requête :
     ```json
     {
       "title": "Inception",
       "director": "Christopher Nolan",
       "year": 2010,
       "genre": "Thriller"
     }
     ```
   - Réponse :
     ```json
     {
       "id": 1,
       "title": "Inception",
       "director": "Christopher Nolan",
       "year": 2010,
       "genre": "Thriller"
     }
     ```

5. **Supprimer un Film**
   - **DELETE** `/{movie_id}`
   - Réponse :
     ```json
     {
       "id": 1,
       "title": "Inception",
       "director": "Christopher Nolan",
       "year": 2010,
       "genre": "Science Fiction"
     }
     ```

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
