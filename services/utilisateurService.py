from werkzeug.security import generate_password_hash
from modeles.modele import utilisateur, db
import os

def inscrire_utilisateur(data): # inscription utilisateur
    nomUtilisateur = data.get('nomUtilisateur')
    prenomUtilisateur = data.get('prenomUtilisateur')
    email = data.get('email')
    motPasse = data.get('motPasse')
    role = data.get('role')

    if utilisateur.query.filter_by(email=email).first():
        return {'erreur': 'email déja existe'}, 400

    motPasse_hash = generate_password_hash(motPasse, os.getenv('HASHPASSWORD')) # generation mot passe crypter
    new_user = utilisateur(
        nomUtilisateur=nomUtilisateur,
        prenomUtilisateur=prenomUtilisateur,
        email=email,
        motPasse=motPasse_hash,
        role=role
    )
    db.session.add(new_user) # ajout nouvel utilisateur
    db.session.commit() # valider

    return {'message': 'utilisateur crée avec succès'}, 201
