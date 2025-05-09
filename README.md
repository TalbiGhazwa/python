<h1 align="center">e-Ticketing System API</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/{{YOUR_GITHUB_USERNAME}}/eticket-api?color=56BEB8">
  <img alt="Github language count" src="https://img.shields.io/github/languages/count/{{YOUR_GITHUB_USERNAME}}/eticket-api?color=56BEB8">
  <img alt="Repository size" src="https://img.shields.io/github/repo-size/{{YOUR_GITHUB_USERNAME}}/eticket-api?color=56BEB8">
  <img alt="License" src="https://img.shields.io/github/license/{{YOUR_GITHUB_USERNAME}}/eticket-api?color=56BEB8">
</p>

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/{{YOUR_GITHUB_USERNAME}}" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

This is a backend REST API built with **Flask** for managing events and ticketing. It supports **user authentication with JWT**, **role-based access (Admin, Client)**, and **CRUD operations** for event and category management. The API is ready for deployment and integrates with a **PostgreSQL** database hosted on Render.

## :sparkles: Features ##

:heavy_check_mark: JWT Authentication (Login/Register);\
:heavy_check_mark: Role-based user management (Admin, Client);\
:heavy_check_mark: Category CRUD (admin-only);\
:heavy_check_mark: Event CRUD (admin-only);\
:heavy_check_mark: Public access to events and categories;\
:heavy_check_mark: PostgreSQL integration.

## :rocket: Technologies ##

This project was developed using the following technologies:

- [Python 3](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-CORS](https://flask-cors.readthedocs.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [Render](https://render.com/) for hosting

## :white_check_mark: Requirements ##

Before starting, you need to have the following installed:

- [Python 3.10+](https://www.python.org/)
- [Git](https://git-scm.com)
- [pip](https://pip.pypa.io/) 

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone https://github.com/TalbiGhazwa/python

# Access the project directory
$ cd python

# (Optional) Create a virtual environment
$ python -m venv venv
$ source venv/bin/activate   

# Install dependencies
$ pip install -r requirements.txt

# Run the app
$ python app.py

# The server will start at http://localhost:5000
