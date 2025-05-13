from modeles.modele import Categories, db, Evenement, utilisateur, comande, panier
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import cross_origin
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from api import api
import pymysql

from src.config.database import init_db
pymysql.install_as_MySQLdb()
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins":"*"}})
init_db(app)

jwt = JWTManager(app)
db.init_app(app)

# creer compte admin
def creer_compte_admin():
    email_admin = os.getenv('ADMINMAIL')
    password_admin = os.getenv('ADMINPASS')
    admin_existe = utilisateur.query.filter_by(email = email_admin).first()
    if not admin_existe:
        password_hashed = generate_password_hash(password_admin, method=os.getenv('HASHPASSWORD'))
        utilisateur_admin = utilisateur(email=email_admin, nomUtilisateur="admin",prenomUtilisateur="admin",motPasse=password_hashed, role="ADMIN")
        db.session.add(utilisateur_admin)
        db.session.commit()
        print("compte ADMIN creer avec succée")
    else:
        print("compte ADMIN déja existe")

with app.app_context():
    db.create_all()
    creer_compte_admin()

app.register_blueprint (api)
if __name__=='__main__':
    app.run(debug=True)