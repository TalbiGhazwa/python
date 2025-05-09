from modeles.modele import Categories, db, Evenement, utilisateur, comande, panier
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import cross_origin
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from api import api
import pymysql
pymysql.install_as_MySQLdb
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins":"*"}})
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:Ghazwa_1993@localhost:3306/eticket'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['JWT_SECRET_KEY']='Ghazwa' #code-clef-secret

jwt = JWTManager(app)
db.init_app(app)

# creer compte admin
def creer_compte_admin():
    email_admin = "admin@admin.com"
    password_admin = "admin789"
    admin_existe = utilisateur.query.filter_by(email = email_admin).first()
    if not admin_existe:
        password_hashed = generate_password_hash(password_admin, method='pbkdf2:sha256')
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