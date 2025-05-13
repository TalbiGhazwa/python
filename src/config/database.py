from modeles.modele import Categories, db, Evenement, utilisateur, comande, panier
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import cross_origin
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from api import api
import pymysql
pymysql.install_as_MySQLdb()
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
    app.config['JWT_SECRET_KEY']=os.getenv('JWT_SECRET_KEY')


   
   



