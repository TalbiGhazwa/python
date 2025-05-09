from modeles.modele import Categories, db, Evenement, utilisateur, comande, panier
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import cross_origin
from flask_cors import CORS
from flask import Flask, jsonify, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
import pymysql

# recherche évènement par id
def get_evenement(id):
    event = Evenement.query.get(id)
    if event:
        return jsonify(event.remplissage())
    return jsonify({'erreur':'evenement pas trouvée'}),404