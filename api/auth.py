
from modeles.modele import  utilisateur
from flask_jwt_extended import create_access_token
from flask_cors import cross_origin
from flask_cors import CORS
from flask import Flask, jsonify, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
import pymysql

cnx = Blueprint('cnx',__name__)

CORS(cnx, resources={r"/*": {"origins":"*"}})

# api connexion utilisateur base sur la role 'admin , client'
@cnx.route('/api/connexion', methods=['POST'])

def connexion():
    data = request.json
    email = data.get('email')
    motPasse = data.get('motPasse')
    role = data.get('role')
    user = utilisateur.query.filter_by(email=email).first()
    if user and user.check_password(motPasse):
        accer_token = create_access_token(identity=str(user.id), fresh=True)
        return jsonify({'access_token':accer_token, "role":user.role}),200 
    return jsonify({'erreur':'invalide'}),401
