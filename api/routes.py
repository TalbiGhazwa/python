from modeles.modele import Categories, db, Evenement, utilisateur,Commande,CommandeItem, TicketType, PanierItem
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager, jwt_required,get_jwt_identity, create_access_token
from flask_cors import cross_origin
from flask_cors import CORS
from flask import Flask, jsonify, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
import pymysql

api = Blueprint('api',__name__)

CORS(api, resources={r"/*": {"origins":"*"}})
from dotenv import load_dotenv
import os

# panier de la client 
@api.route('/api/commandePanier', methods=['POST'])
@jwt_required()
def ajouter_au_panier():
    data = request.json
    utilisateur_id = get_jwt_identity()
    evenement_id = data.get('evenement_id')
    ticket_type_nom = data.get('ticket_type_nom')
    quantite = data.get('quantite', 1)
    prix = data.get('prix') 

    if not evenement_id or not ticket_type_nom:
        return jsonify({'erreur': 'Les champs evenement_id et ticket_type_nom sont requis'}), 400

    evenement = Evenement.query.get(evenement_id)
    if not evenement:
        return jsonify({'erreur': 'Événement introuvable'}), 404

    # Vérife si le type de ticket existe deja pour cet événement
    ticket_type = TicketType.query.filter_by(nom=ticket_type_nom, evenement_id=evenement_id).first()

    # crée nouveau type de ticket 
    if not ticket_type:
        if prix is None:
            return jsonify({'erreur': 'Le prix est requis pour créer un nouveau type de ticket'}), 400
        ticket_type = TicketType(nom=ticket_type_nom, prix=prix, evenement_id=evenement_id)
        db.session.add(ticket_type)
        db.session.commit()

    # Vérifie si l'article existe déjà dans le panier
    item_existant = PanierItem.query.filter_by(
        utilisateur_id=utilisateur_id,
        evenement_id=evenement_id,
        ticket_type_id=ticket_type.id
    ).first()

    if item_existant:
        item_existant.quantite += quantite  
        item_existant.total_prix = item_existant.quantite * ticket_type.prix  #Calculer  la prix total d tout produit 
    else:
        item_existant = PanierItem(
            utilisateur_id=utilisateur_id,
            evenement_id=evenement_id,
            ticket_type_id=ticket_type.id,
            quantite=quantite,
            total_prix=quantite * ticket_type.prix
        )
        db.session.add(item_existant)

    db.session.commit()

    return jsonify({'message': 'Article ajouté au panier avec succès'}), 201

# vider le panier apré la validation de comande
@api.route('/api/commande/supprimer', methods=['DELETE'])
@jwt_required()
def supprimer_commandes():
    utilisateur_id = get_jwt_identity()
    
    # Récupérer toutes les commandes de l'utilisateur
    commandes = Commande.query.filter_by(utilisateur_id=utilisateur_id).all()

    for commande in commandes:
        # Supprimer les items liés à chaque commande
        CommandeItem.query.filter_by(commande_id=commande.id).delete()

        # Supprimer la commande même
        db.session.delete(commande)
    db.session.commit()
    return jsonify({'message': 'Commandes supprimées avec succès'}), 200

# recupere l'information de commande client 
@api.route('/api/commandePanier/commande/info', methods=['GET'])
@jwt_required()
def commande_info():
    utilisateur_id = get_jwt_identity()
    commandes = Commande.query.filter_by(utilisateur_id=utilisateur_id).all()

    resultat = []
    for commande in commandes:
        items = CommandeItem.query.filter_by(commande_id=commande.id).all()
        item_details = []

        for item in items:
            ticket_type = TicketType.query.get(item.ticket_type_id)
            evenement = Evenement.query.filter_by(id=ticket_type.evenement_id).first() if ticket_type else None

            item_details.append({
                'quantite': item.quantite,
                'ticket_type': {
                    'id': ticket_type.id,
                    'nom': ticket_type.nom,
                    'prix': ticket_type.prix
                } if ticket_type else None,
                'evenement': {
                    'id': evenement.id,
                    'nomEvenement': evenement.nomEvenement,
                    'dateEvenement': evenement.dateEvenement,
                    'typeEvenement': evenement.typeEvenement,
                    'PrixEvenement': evenement.PrixEvenement,
                    'adresse': evenement.adresse
                } if evenement else None
            })

        resultat.append({
            'commande_id': commande.id,
            'total': commande.total,
            'date_commande': commande.date_creation if hasattr(commande, 'date_creation') else 'N/A',
            'items': item_details
        })
    return jsonify(resultat), 200

#recupere information de la utilisateur connecte
@api.route('/api/commandePanier/utilisateur/info', methods=['GET'])
@jwt_required()
def info_utilisateur():
    utilisateur_id = get_jwt_identity()
    user = utilisateur.query.get(utilisateur_id)

    if not user:
        return jsonify({'erreur': 'Utilisateur non trouvé'}), 404

    return jsonify({
        'nom': user.nomUtilisateur,
        'prenom': user.prenomUtilisateur,
        'email': user.email
    })

#valider la commande 
@api.route('/api/commande/valider', methods=['POST'])
@jwt_required()
def valider_commande_utilisateur():
    utilisateur_id = get_jwt_identity()

    # Récupérer les articles du panier
    panier_items = PanierItem.query.filter_by(utilisateur_id=utilisateur_id).all()
    if not panier_items:
        return jsonify({'erreur': 'Le panier est vide'}), 400

    # Calculer le total 
    total = sum(item.total_prix for item in panier_items)

    # Créer la commande
    nouvelle_commande = Commande(utilisateur_id=utilisateur_id, total=total)
    db.session.add(nouvelle_commande)
    db.session.commit()

    # Créer les items de la commande
    for item in panier_items:
        commande_item = CommandeItem(
            commande_id=nouvelle_commande.id,
            ticket_type_id=item.ticket_type_id,
            quantite=item.quantite
        )
        db.session.add(commande_item)

    # Vider le panier
    for item in panier_items:
        db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Commande validée avec succès', 'commande_id': nouvelle_commande.id}), 201

# api connexion utilisateur base sur la role 'admin , client'
@api.route('/api/connexion', methods=['POST'])

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

#calculer la nomber des element existe dans la panier 
@api.route('/api/commandePanier/count', methods=['GET'])
@jwt_required()
def get_panier_count():
    user_id = get_jwt_identity()  # récupère id utilisateur du token JWT
    count = PanierItem.query.filter_by(utilisateur_id=user_id).count()
    return jsonify({'count': count})

#afficher l information de la panier  
@api.route('/api/commandePanier/view', methods=['GET'])
@jwt_required()
def afficher_panier_utilisateur():
    utilisateur_id = get_jwt_identity()
    items = PanierItem.query.filter_by(utilisateur_id=utilisateur_id).all()

    resultat = []
    for item in items:
        ticket_type = TicketType.query.get(item.ticket_type_id)
        evenement = Evenement.query.get(item.evenement_id)

        resultat.append({
            'id': item.id,
            'quantite': item.quantite,
            'ticket_type': {
                'id': ticket_type.id,
                'nom': ticket_type.nom,
                'prix': ticket_type.prix
            } if ticket_type else None,
            'evenement': {
                'id': evenement.id,
                'nomEvenement': evenement.nomEvenement,
                'dateEvenement': evenement.dateEvenement,
                'typeEvenement': evenement.typeEvenement,
                'PrixEvenement': evenement.PrixEvenement,
                'adresse': evenement.adresse
            } if evenement else None
        })

    return jsonify(resultat), 200

# recuperer tout les utilisateur de role ="client"
@api.route('/api/admin/clients', methods=['GET'])
@jwt_required()
def get_client():
    clients = utilisateur.query.filter_by(role="CLIENT").all()
    return jsonify([{
        'id' : client.id,
        'nomUtilisateur' : client.nomUtilisateur,
        'prenomUtilisateur':client.prenomUtilisateur,
        'email' : client.email,
        'role' : client.role,
        }
        for client in clients
    ]),200

# afficher le categorie de la evenement pour tout visiteur non authentifier
@api.route('/api/public/categori',methods=['GET'])
def public_get_categorie():
    Categorie = Categories.query.all()
    return jsonify([{
        'id' : cat.id,
        'nomCategori' : cat.nomCategori
    }
    for cat in Categorie
    ]),200

#pour un accée public a tout les evenement
@api.route('/api/public/evenements',methods=['GET'])
def get_all_evenement():
    events = Evenement.query.all()
    return jsonify([{
        'id' : E.id,
        'nomEvenement' : E.nomEvenement,
        'typeEvenement' : E.typeEvenement,
        'dateEvenement' : E.dateEvenement,
        'PrixEvenement' : E.PrixEvenement,
        'categorie' : {'id' : E.categorie.id, 'nomCategori' : E.categorie.nomCategori} if E.categorie else None

    } for E in events
    ]),200

#recupere le infromation de l'evenement pour tous le utilisateur public 
@api.route('/api/public/evenements/<int:id>', methods=['GET'])
def get_evenement(id):
    event = Evenement.query.get(id)
    if event:
        return jsonify(event.remplissage())
    return jsonify({'erreur':'evenement pas trouvée'}),404

#recupere le infromation de la categories par id 
@api.route('/api/categori/<int:id>',methods=['GET'])
@jwt_required()
def manage_categorie_id(id):
        categori = Categories.query.get(id)
        if categori:
            return jsonify({'id':categori.id,'nomCategori':categori.nomCategori}),200
        return jsonify({'erreur':'categorie non trouvée'}),404

# admin recupere tout categorie
@api.route('/api/admin/categori',methods=['GET'])
@jwt_required()
def get_cat_admin():
    cat = Categories.query.all()
    return jsonify([{
        'id': c.id,
        'nomCategori': c.nomCategori
    } for c in cat]), 200


# admin ajoute une categorie
@api.route('/api/admin/categori',methods=['POST'])
@jwt_required()
def ajout_cat():
    data = request.json
    nom_categorie = data.get('nomCategori')
    if not nom_categorie:
        return jsonify({'erreur':'nom categorie requis'}),400
    if Categories.query.filter_by(nomCategori=nom_categorie).first():
        return jsonify({'erreur':'categorie existe déjà'}),400
    new_cat = Categories(nomCategori=nom_categorie)
    db.session.add(new_cat)
    db.session.commit()
    return jsonify({'message':'categorie ajoutée avec succès'}),201

#admin modifier la categorie
@api.route('/api/admin/categori/<int:id>', methods=['PUT'])
@jwt_required()
def modifier_categorie(id):
    categorie = Categories.query.get(id)
    if not categorie:
        return jsonify({'erreur': 'categorie non trouvée'}),404
    data = request.json
    nom = data.get('nomCategori')
    if not nom:
        return jsonify({'erreur': 'nom categorie requis'}),400
    if Categories.query.filter(Categories.nomCategori == nom, Categories.id != id).first():
        return jsonify({'erreur': 'categorie avec ce nom existe déjà'}),400
    categorie.nomCategori = nom
    db.session.commit()
    return jsonify({'message': 'categorie modifiée avec succès'}),200
 
# admin recupere tout les evenement
@api.route('/api/admin/evenements', methods=['GET'])
@jwt_required()

def get_evenement_admin():
    event = Evenement.query.all()
    return jsonify([
        {
            'id': E.id,
            'nomEvenement': E.nomEvenement,
            'typeEvenement': E.typeEvenement,
            'dateEvenement': E.dateEvenement,
            'PrixEvenement': E.PrixEvenement,
            'adresse' : E.adresse,
            'categorie':{
                'id_categori': E.categorie.id,
                'nomCategori': E.categorie.nomCategori}if E.categorie else None
        }for E in event
            ]),200

# admin ajouter nouvelle evenement
@api.route('/api/admin/evenements', methods=['POST'])
@jwt_required()
def ajout_evenement():
    data = request.json
    print("données reçues :", data)  

    #  verifier si tout f.require et présent
    champs_requis = ['nomEvenement', 'typeEvenement', 'dateEvenement', 'PrixEvenement', 'adresse', 'category_id']
    champs_manquants = [champ for champ in champs_requis if champ not in data or not data[champ]]

    if champs_manquants:
        print(f"Champs manquants: {', '.join(champs_manquants)}")  
        return jsonify({'erreur': f'champs manquants : {", ".join(champs_manquants)}'}), 400

    # Verifier si la catégorie existe
    cat = Categories.query.get(data['category_id'])
    if not cat:
        print(f"Catégorie non trouvée pour l'ID {data['category_id']}")  
        return jsonify({'erreur': 'Catégorie non trouvée'}), 404

    # crée evenement
    nouvel_evenement = Evenement(
        nomEvenement=data['nomEvenement'],
        typeEvenement=data['typeEvenement'],
        dateEvenement=data['dateEvenement'],
        PrixEvenement=data['PrixEvenement'],
        adresse=data['adresse'],
        categorie=cat
    )
    db.session.add(nouvel_evenement)
    db.session.commit()
    return jsonify({'message': 'Événement créé avec succès'}), 201

#admin peur supprimer ou modifeir evenement
@api.route('/api/admin/evenements/<int:id>', methods=['PUT','DELETE'])
@jwt_required()
def mise_ajour_supprim_evenement(id):
    event = db.session.get(Evenement,id)
    if not event:
        return jsonify({'erreur':'evenement pas trouvée'}),404
    
    # modifier evenement
    if request.method == 'PUT':
        data = request.json
        print('donner modifie:', data)

        event.nomEvenement = data.get('nomEvenement',event.nomEvenement)
        event.typeEvenement = data.get('typeEvenement',event.typeEvenement)
        event.dateEvenement = data.get('dateEvenement',event.dateEvenement)
        event.PrixEvenement = data.get('PrixEvenement',event.PrixEvenement)
        event.adresse = data.get('adresse', event.adresse)
        event.category_id = data.get('category_id',event.category_id)

        db.session.commit()
        return jsonify ({'mesage':'evenement modifier avec succée'}),200
    
    elif request.method == 'DELETE':
        db.session.delete(event)
        db.session.commit()
        return jsonify ({'mesage':'evenement supprimer avec succée'}),200
    
#admin recupere categories par id  
@api.route('/api/admin/categori/<int:id>', methods=['GET'])
@jwt_required()
def get_categorie_by_id(id):
    categori = Categories.query.get(id)
    if categori:
        return jsonify({'id': categori.id, 'nomCategori': categori.nomCategori}), 200
    return jsonify({'erreur': 'categorie non trouvée'}), 404
@api.route('/api/admin/categori/<int:id>', methods=['DELETE'])
def delete_categorie(id):
    categori = Categories.query.get(id)
    if not categori:
        return jsonify({'erreur': 'categorie non trouvée'}), 404

    #  supprimer evenement associé
    Evenement.query.filter_by(category_id=id).delete()

    # supprimer categorie
    db.session.delete(categori)
    db.session.commit()
    return jsonify({'message': 'categorie et evenements associés supprimés avec succès'}), 200

# admin recuepere tous les client
@api.route('/api/admin/utilisateurs', methods=['GET'])
@jwt_required()
def get_all_utilisateurs():
    utilisateurs_list = utilisateur.query.all()
    return jsonify([
        {
            'id': u.id,
            'nomUtilisateur': u.nomUtilisateur,
            'prenomUtilisateur': u.prenomUtilisateur,
            'email': u.email,
            'role': u.role
        }
        for u in utilisateurs_list
    ]), 200
