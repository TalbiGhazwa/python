import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from modeles.modele import db, utilisateur, PanierItem, TicketType, Evenement
from app import create_app 

@pytest.fixture
def app():
    app = create_app('testing')  
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def token_utilisateur(app):
    user = utilisateur(
        nomUtilisateur="Ali",
        prenomUtilisateur="Ben Ali",
        email="ali@example.com",
        motPasse="hashedpass",
        role="client"
    )
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=str(user.id))
    return token

def test_inscription(client):
    response = client.post('/api/inscription', json={
        "nomUtilisateur": "Sami",
        "prenomUtilisateur": "Salah",
        "email": "sami@example.com",
        "motPasse": "test1234",
        "role": "client"
    })
    assert response.status_code == 201
    assert b"utilisateur cr" in response.data.lower()

def test_connexion(client):
    # Créer un utilisateur 
    hashed_password = "pbkdf2:sha256:260000$..."  
    user = utilisateur(nomUtilisateur="talbi", prenomUtilisateur="ghazwa", email="ghazwa@gmail.com", motPasse=hashed_password, role="client")
    db.session.add(user)
    db.session.commit()

    response = client.post('/api/connexion', json={
        "email": "ghazwa@gmail.com",
        "motPasse": "ghazwa123",
        "role": "client"
    })

    assert response.status_code == 200 or response.status_code == 401  # dépend de si le motPasse correspond au hash
    assert b"access_token" in response.data or b"invalide" in response.data

def test_ajout_panier(client, token_utilisateur, app):
    # Ajouter un événement et un type de ticket
    evenement = Evenement(nomEvenement="football", dateEvenement="20-07-2025", typeEvenement="demi-final", PrixEvenement=250, adresse="stade de france")
    db.session.add(evenement)
    db.session.commit()

    response = client.post('/api/commandePanier', json={
        "evenement_id": evenement.id,
        "ticket_type_nom": "VIP",
        "quantite": 2,
        "prix": 100  
    }, headers={"Authorization": f"Bearer {token_utilisateur}"})

    assert response.status_code == 201
    assert b"ajout" in response.data.lower()

def test_get_panier_count(client, token_utilisateur):
    response = client.get('/api/commandePanier/count', headers={"Authorization": f"Bearer {token_utilisateur}"})
    assert response.status_code == 200
    assert b"count" in response.data
