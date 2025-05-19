from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import pymysql
import os
from modeles.modele import Categories, Evenement, utilisateur, db, TicketType, PanierItem, Commande, CommandeItem

from api import api

from src.config.database import init_db

import pymysql

from src.config.database import init_db
pymysql.install_as_MySQLdb()
from dotenv import load_dotenv
import os

load_dotenv()  

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins":"*"}})
init_db(app)

jwt = JWTManager(app)
db.init_app(app)
@api.route('/api/commandePanier/panier', methods=['POST'])
@jwt_required()
def ajouter_panier():
    user_id = get_jwt_identity()
    data = request.json
    ticket_type_id = data.get('ticket_type_id')
    quantite = data.get('quantite', 1)

    ticket = TicketType.query.get(ticket_type_id)
    if not ticket:
        return jsonify({'erreur': 'Ticket non trouvé'}), 404

    item = PanierItem.query.filter_by(utilisateur_id=user_id, ticket_type_id=ticket_type_id).first()
    if item:
        item.quantite += quantite
    else:
        item = PanierItem(utilisateur_id=user_id, ticket_type_id=ticket_type_id, quantite=quantite)
        db.session.add(item)

    db.session.commit()
    return jsonify({'message': 'Ajouté au panier'}), 201
@api.route('/api/commandePanier/panier', methods=['GET'])
@jwt_required()
def afficher_panier():
    user_id = get_jwt_identity()
    items = PanierItem.query.filter_by(utilisateur_id=user_id).all()
    return jsonify([
        {
            'id': item.id,
            'ticket_type': item.ticket_type.nom,
            'prix': item.ticket_type.prix,
            'quantite': item.quantite,
            'total': item.ticket_type.prix * item.quantite
        } for item in items
    ]), 200
@api.route('/api/commandePanier/valider_commande', methods=['POST'])
@jwt_required()
def valider_commande():
    user_id = get_jwt_identity()
    panier = PanierItem.query.filter_by(utilisateur_id=user_id).all()
    if not panier:
        return jsonify({'erreur': 'Panier vide'}), 400

    total = sum(item.ticket_type.prix * item.quantite for item in panier)
    commande = Commande(utilisateur_id=user_id, total=total)
    db.session.add(commande)
    db.session.flush()  # obtenir ID commande sans commit

    for item in panier:
        commande_item = CommandeItem(
            commande_id=commande.id,
            ticket_type_id=item.ticket_type_id,
            quantite=item.quantite
        )
        db.session.add(commande_item)

    PanierItem.query.filter_by(utilisateur_id=user_id).delete()
    db.session.commit()
    return jsonify({'message': 'Commande validée', 'total': total}), 201

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