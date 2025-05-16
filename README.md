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
- Accès public aux événements, et aux catégories disponibles

---

## :sparkles: Features ##

:heavy_check_mark: Authentification JWT ;  
:heavy_check_mark: Rôles utilisateurs (admin, client) ;  
:heavy_check_mark: CRUD événements pour admin ;  
:heavy_check_mark: CRUD catégories pour admin ;  
:heavy_check_mark: Accès public aux événements ;  
:heavy_check_mark: Intégration PostgreSQL ;  

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
 
- [Python](https://www.python.org/)  
- [pip](https://pip.pypa.io/)  
- [GIT](https://git-scm.com) 


## :checkered_flag: Starting ##


# Cloner le projet
```bash
$ git clone https://github.com/TalbiGhazwa/python
```
# Accéder au dossier du projet
```bash
$ cd python
```
# Créer et activer un environnement virtuel
```bash
$ python -m venv venv
$ source venv/bin/activate   
```
# Installer les dépendances
```bash
$ pip install -r requirements.txt
```
# Lancer le projet
```bash
$ python app.py
```
# Serveur accessible sur :
`http://localhost:4200`
## :gear: API Endpoints ##

### 🔗 URL de Base
`http://127.0.0.1:5000/api/`

---

### 🔐 Authentification

#### 1. **Inscription d'utilisateur**
- **Méthode :** POST  
- **URL :** `/api/inscription`  
- **Corps de la requête :**
```json
{
  "nomUtilisateur": "Dupon",
  "prenomUtilisateur": "Jean",
  "email": "DuponJean@gmail.com",
  "motPasse": "jean123",
  "role": "CLIENT"
}
```
- **Réponse :**
```json
{
  "message": "Utilisateur inscrit avec succès"
}
```

#### 2. **Connexion**
- **Méthode :** POST  
- **URL :** `/api/connexion`  
- **Corps de la requête :**
```json
{
  "email": "DuponJean@gmail.com",
  "motPasse": "jean123",
  "role": "CLIENT"
}
```
- **Réponse :**
```json
{
  "access_token": "eyJ0eX....."
}
```

---

### 🧑‍💼 Admin : Catégories

#### 3. **Ajouter une catégorie**
- **Méthode :** POST  
- **URL :** `/api/admin/categori`  
- **Corps de la requête :**
```json
{
  "nomCategori": "Sport"
}
```
- **Réponse :**
```json
{
  "message": "categorie ajouté avec succée"
}
```

#### 4. **Modifier une catégorie**
- **Méthode :** PUT  
- **URL :** `/api/admin/categori/1`  
- **Corps de la requête :**
```json
{
  "nomCategori": "Sport"
}
```
- **Réponse :**
```json
{
  "message": "modification effectuer avec succée"
}
```

#### 5. **Supprimer une catégorie**
- **Méthode :** DELETE  
- **URL :** `/api/admin/categori/1`  
- **Corps de la requête :**
```json
{
  "nomCategori": "Sport"
}
```
- **Réponse :**
```json
{
  "message": "categori supprimer avec succée"
}
```

---

### 🧑‍💼 Admin : Événements

#### 6. **Ajouter un évènement**
- **Méthode :** POST  
- **URL :** `/api/admin/evenements`  
- **Corps de la requête :**
```json
{
  "nomEvenement": "France - espagne",
  "typeEvenement": "football",
  "dateEvenement": "10-06-2025",
  "PrixEvenement": "500",
  "adresse": "stade de france",
  "category_id": 1
}
```
- **Réponse :**
```json
{
  "message": "Evenement ajouter avec succée"
}
```

#### 7. **Modifier un évènement**
- **Méthode :** PUT  
- **URL :** `/api/admin/evenements/1`  
- **Corps de la requête :**
```json
{
  "nomEvenement": "France - espagne",
  "typeEvenement": "football",
  "dateEvenement": "10-06-2025",
  "PrixEvenement": 600,
  "adresse": "stade de france",
  "category_id": 1
}
```
- **Réponse :**
```json
{
  "message": "Evenement modifier avec succée"
}
```

#### 8. **Supprimer un évènement**
- **Méthode :** DELETE  
- **URL :** `/api/admin/evenements/1`  
- **Corps de la requête :**
```json
{
  "nomEvenement": "France - espagne",
  "typeEvenement": "football",
  "dateEvenement": "10-06-2025",
  "PrixEvenement": 600,
  "adresse": "stade de france",
  "category_id": 1
}
```
- **Réponse :**
```json
{
  "message": "Evenement supprimer avec succée"
}
```

---

### 🧑‍💼 Admin : Utilisateurs

#### 9. **Récupérer tous les utilisateurs**
- **Méthode :** GET  
- **URL :** `/api/admin/clients`  
- **Réponse :**
```json
[
  {
    "id": 1,
    "nomUtilisateur": "Dupon",
    "prenomUtilisateur": "Jean",
    "email": "DuponJean@gmail.com",
    "motPasse": "jean123",
    "role": "CLIENT"
  },
  {
    "nomUtilisateur": "garnier",
    "prenomUtilisateur": "isabelle",
    "email": "DuponJean@gmail.com",
    "motPasse": "isabelle123",
    "role": "CLIENT"
  }
]
```

---

### 🌐 Public

#### 10. **Récupérer liste des catégories**
- **Méthode :** GET  
- **URL :** `/api/public/categori`  
- **Réponse :**
```json
[
  {
    "id": 1,
    "nomCategori": "football"
  },
  {
    "id": 2,
    "nomCategori": "handball"
  }
]
```

#### 11. **Récupérer liste des évènements**
- **Méthode :** GET  
- **URL :** `/api/public/evenements`  
- **Réponse :**
```json
[
  {
    "id": 1,
    "nomEvenement": "France - espagne",
    "typeEvenement": "football",
    "dateEvenement": "10-06-2025",
    "PrixEvenement": 600,
    "adresse": "stade de france",
    "category_id": 1
  }
]
```

#### 12. **Détail d'un évènement**
- **Méthode :** GET  
- **URL :** `/api/public/evenements/1`  
- **Réponse :**
```json
{
  "id": 1,
  "nomEvenement": "France - espagne",
  "typeEvenement": "football",
  "dateEvenement": "10-06-2025",
  "PrixEvenement": 600,
  "adresse": "stade de france",
  "category_id": 1
}
```