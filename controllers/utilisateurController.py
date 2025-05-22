from flask import Blueprint, request, jsonify
from services.utilisateurService import inscrire_utilisateur

utilisateur_controller = Blueprint('utilisateur_controller', __name__)

@utilisateur_controller.route('/api/inscription', methods=['POST'])
def inscription():
    data = request.json
    response, status_code = inscrire_utilisateur(data)
    return jsonify(response), status_code
