from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

import datetime
import pymysql
pymysql.install_as_MySQLdb

db = SQLAlchemy()
class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomCategori = db.Column(db.String(255), unique=True, nullable=False)
 
    def __repr__(self):
        return f'<categories{self.nomCategori}>'
    
class Evenement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomEvenement = db.Column(db.String(255), nullable=False)
    typeEvenement = db.Column(db.String(255), nullable=False)
    dateEvenement = db.Column(db.String(255), nullable=False)
    PrixEvenement = db.Column(db.String(255), nullable=False)
    adresse = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    categorie = db.relationship('Categories', backref=db.backref('evenements',lazy=True))

    def remplissage(self):
        return{
            'id' : self.id,
            'nomEvenement' : self.nomEvenement,
            'typeEvenement' : self.typeEvenement,
            'dateEvenement' : self.dateEvenement,
            'PrixEvenement' : self.PrixEvenement,
            'adresse':self.adresse,
            'categorie':{
                'id_categori' : self.categorie.id,
                'nomCategori' : self.categorie.nomCategori
            }


        }

class utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomUtilisateur = db.Column(db.String(255), nullable=False)
    prenomUtilisateur = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255),unique=True, nullable=False)
    motPasse = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable= False)

    def check_password(self, password):
        return check_password_hash(self.motPasse, password)



class TicketType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)  # ex: Classe A, Classe B, Familial
    prix = db.Column(db.Float, nullable=False)
    evenement_id = db.Column(db.Integer, db.ForeignKey('evenement.id'), nullable=False)
    evenement = db.relationship('Evenement', backref=db.backref('ticket_types', lazy=True))

class PanierItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))
    evenement_id = db.Column(db.Integer, db.ForeignKey('evenement.id'))
    ticket_type_id = db.Column(db.Integer, db.ForeignKey('ticket_type.id'))
    quantite = db.Column(db.Integer, default=1)
    total_prix = db.Column(db.Float)  

class Commande(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    date_commande = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    total = db.Column(db.Float, nullable=False)

    utilisateur = db.relationship('utilisateur')

class CommandeItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'), nullable=False)
    ticket_type_id = db.Column(db.Integer, db.ForeignKey('ticket_type.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)

    ticket_type = db.relationship('TicketType')
    commande = db.relationship('Commande', backref=db.backref('items', lazy=True))


 