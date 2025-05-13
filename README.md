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
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/TalbiGhazwa" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

Il s'agit d'un back-end développé avec "Flask" pour la gestion des évènement et  billéterie.
l'authentification avec JWT avec un accés selon le role d'utilisateur administrateur ou client.
des opérations pour la gestion des évènements et des catégories( CRUD ).


## :sparkles: Features ##

:heavy_check_mark: authentification JWT ;\
:heavy_check_mark: gestion des utilisateus selon le role( administrateur, client);\
:heavy_check_mark: opérations CRUD aux évènements pour admin ;\
:heavy_check_mark: opérations CRUD aux catégories pour admin ;\
:heavy_check_mark: accé public pour les évènements disponibles ;\
:heavy_check_mark: Intégration de BD PostgreSQL ;\

## :gear: API Endpoints (JSON Format) ##

```json
[
  {
    "method": "POST",
    "url": "/api/inscription",
    "description": "Créer un nouvel utilisateur (inscription)",
    "access": "Public"
  },
  {
    "method": "POST",
    "url": "/api/connexion",
    "description": "Connexion d'un utilisateur avec retour de JWT",
    "access": "Public"
  },
  {
    "method": "GET",
    "url": "/api/admin/clients",
    "description": "Récupérer tous les clients",
    "access": "Admin (JWT requis)"
  },
  {
    "method": "GET",
    "url": "/api/public/categori",
    "description": "Lister toutes les catégories (public)",
    "access": "Public"
  },
  {
    "method": "GET",
    "url": "/api/public/evenements",
    "description": "Lister tous les événements disponibles (public)",
    "access": "Public"
  },
  {
    "method": "GET",
    "url": "/api/public/evenements/<id>",
    "description": "Récupérer un événement par ID",
    "access": "Public"
  },
  {
    "method": "GET",
    "url": "/api/categori/<id>",
    "description": "Récupérer une catégorie par ID",
    "access": "JWT requis"
  },
  {
    "method": "GET",
    "url": "/api/admin/categori",
    "description": "Récupérer toutes les catégories (admin)",
    "access": "Admin (JWT requis)"
  },
  {
    "method": "POST",
    "url": "/api/admin/categori",
    "description": "Ajouter une nouvelle catégorie (admin)",
    "access": "Admin (JWT requis)"
  },
  {
    "method": "PUT",
    "url": "/api/admin/categori/<id>",
    "description": "Modifier une catégorie par ID (admin)",
    "access": "Admin (JWT requis)"
  },
  {
    "method": "DELETE",
    "url": "/api/admin/categori/<id>",
    "description": "Supprimer une catégorie par ID (admin)",
    "access": "Admin (JWT requis)"
  }
]


## :rocket: Technologies ##

The following tools were used in this project:

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/)
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [Render](https://render.com/)


## :white_check_mark: Requirements ##

Avant de démarrer vous devez avoir [GIT](https://git-scm.com) , [Python](https://www.python.org/) et [pip](https://pip.pypa.io/) installés.

## :checkered_flag: Starting ##

```bash
# Cloner le project
$ git clone https://github.com/TalbiGhazwa/python

# Accée au projet
$ cd python

# créer un environnement virtuel
$ python -m venv venv
$ source venv/bin/activate

# Installer les dependences
$ pip install -r requirements.txt

# Run le projet
$ python app.py

# Le serveur s'initialisera dans <http://localhost:4200>
```

## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE) file.


Made with :heart: by <a href="https://github.com/TalbiGhazwa" target="_blank">TALBI Ghazwa</a>

&#xa0;

<a href="#top">Back to top</a>
