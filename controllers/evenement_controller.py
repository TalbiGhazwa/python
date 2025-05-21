# controllers/evenement_controller.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from modeles.modele import Evenement, Categories, db

evenement_bp = Blueprint('evenement_bp', __name__)

# Obtener tous les événements
@evenement_bp.route('/api/evenements', methods=['GET'])
def get_evenements():
    evenements = Evenement.query.all()
    return jsonify([e.remplissage() for e in evenements]), 200

# crée nouveau evenement
@evenement_bp.route('/api/evenements', methods=['POST'])
@jwt_required()
def create_evenement():
    data = request.json
    nom = data.get('nomEvenement')
    typeE = data.get('typeEvenement')
    date = data.get('dateEvenement')
    prix = data.get('PrixEvenement')
    adresse = data.get('adresse')
    categorie_id = data.get('category_id')

    if not Categories.query.get(categorie_id):
        return jsonify({'error': 'Catégorie non trouvée'}), 404

    evenement = Evenement(
        nomEvenement=nom,
        typeEvenement=typeE,
        dateEvenement=date,
        PrixEvenement=prix,
        adresse=adresse,
        category_id=categorie_id
    )
    db.session.add(evenement)
    db.session.commit()

    return jsonify({'message': 'Événement créé avec succès'}), 201

# supprimer evenement id
@evenement_bp.route('/api/evenements/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_evenement(id):
    evenement = Evenement.query.get(id)
    if not evenement:
        return jsonify({'error': 'Événement non trouvé'}), 404

    db.session.delete(evenement)
    db.session.commit()
    return jsonify({'message': 'Événement supprimé avec succès'}), 200
