from modeles.modele import Categories, db, Evenement, utilisateur, comande, panier
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import cross_origin
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins":"*"}})
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://eticket_wqua_user:OiYFq2LsyYYd7oPYt87dzuVTBbkGl2VO@dpg-cvq3gnje5dus73f0mcsg-a.oregon-postgres.render.com/eticket_wqua'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['JWT_SECRET_KEY']='Ghazwa' #code-clef-secret

jwt = JWTManager(app)
db.init_app(app)

# creer compte admin
def creer_compte_admin():
    email_admin = "admin@admin.com"
    password_admin = "admin789"
    admin_existe = utilisateur.query.filter_by(email = email_admin).first()
    if not admin_existe:
        password_hashed = generate_password_hash(password_admin, method='pbkdf2:sha256')
        utilisateur_admin = utilisateur(email=email_admin, nomUtilisateur="admin",prenomUtilisateur="admin",motPasse=password_hashed, role="ADMIN")
        db.session.add(utilisateur_admin)
        db.session.commit()
        print("compte ADMIN creer avec succée")
    else:
        print("compte ADMIN déja existe")

with app.app_context():
    db.create_all()
    creer_compte_admin()


@app.route('/api/inscription', methods=['POST'])


def inscription():
    data = request.json
    nomUser = data.get('nomUtilisateur'),
    prenomUser = data.get('prenomUtilisateur'),
    email = data.get('email'),
    mpass = data.get('motPasse'),
    role = data.get('role')

    if utilisateur.query.filter_by(email=email).first():
        return jsonify({'erreur':'email déja existe'}),400
    
    mPass_hash = generate_password_hash(mpass, method='pbkdf2:sha256')
    new_utilisateur = utilisateur(
        nomUtilisateur = nomUser,
        prenomUtilisateur = prenomUser,
        email = email,
        mpass = mPass_hash,
        role = role
    )
    db.session.add(new_utilisateur)
    db.session.commit()

    return jsonify({'message' : 'utilisateur crée avec succée'}),201

@app.route('/api/connexion', methods=['POST'])

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

# recuperer tout les utilisateur de role ="client"
@app.route('/api/utilisateur/clients', methods=['GET'])

@jwt_required()

def get_client():
    clients = utilisateur.query.filter_by(role="CLIENT").all()
    return jsonify([{
        'id' : client.id,
        'nomUtilisateur' : client.nomUtilisateur,
        'prenomUtilisateur':client.prenomUtilisateur,
        'email' : client.email
        }
        for client in clients
    ]),200

# pour tout visiteurs non authentifier
@app.route('/api/public/categori',methods=['GET'])


def public_get_categorie():
    Categorie = Categories.query.all()
    return jsonify([{
        'id' : cat.id,
        'nomCategori' : cat.nomCategori
    }
    for cat in Categorie
    ]),200

#pour un accée public a tout les evenement
@app.route('/api/public/evenements',methods=['GET'])


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

@app.route('/api/public/evenements/<int:id>', methods=['GET'])


def get_evenement(id):
    event = Evenement.query.get(id)
    if event:
        return jsonify(event.remplissage())
    return jsonify({'erreur':'evenement pas trouvée'}),404

#accée public categorie_id
@app.route('/api/categori/<int:id>',methods=['GET'])

@jwt_required()

def manage_categorie_id():
        categori = Categories.query.get(id)
        if categori:
            return jsonify({'id':categori.id,'nomCategori':categori.nomCategori}),200
        return jsonify({'erreur':'categorie non trouvée'}),404
("""
    if request.method == 'POST':
        data = request.json
        cat_name = data.get('nomCategori')
        if not cat_name:
            return jsonify({'erreur': 'nom categorie requise'}),400
        if Categories.query.filter_by(nomCategori=cat_name).first():
            return jsonify({'erreur':'categorie existe'}),400
        
        new_cat = Categories(nomCategori=cat_name)
        db.session.add(new_cat)
        db.session.commit()
        return jsonify({'message':'categorie ajouter avec succée'}),201
""")

@app.route('/api/admin/categori',methods=['GET'])

@jwt_required

def get_cat_admin():
    cat = Categories.query.all()
    return jsonify({'id':cat.id, 'nomCategori':cat.nomCategori}),200

#que admin peut ajouter une categorie
@app.route('/api/admin/categori',methods=['POST'])

@jwt_required()

def ajout_cat():
    data = request.json
    nom_categorie = data.get('nomCategori')
    if not nom_categorie:
        return jsonify({'erreur':'categorie pas trouvée'}),400
    if Categories.query.filter_by(nomCategori=nom_categorie).first():
        return jsonify({'erreur':'categorie existe pas'}),400
    new_cat = Categories(nomCategori=nom_categorie)
    db.session.add(new_cat)
    db.session.commit()
    return jsonify ({'mesage':'categorie ajoutée avec succée'}),201

#admin modif || supprime categorie
@app.route('/api/admin/categori/<int:id>',methods=['PUT','DELETE'])

@jwt_required()

def mis_jour_supprim_cat(id):
    cat = Categories.query.get(id)
    if not cat:
        return jsonify({'erreur':'categorie non trouvée'}),404
    
    if request.method == 'PUT':
        data = request.json
        cat.nomCategori =data.get('nomCategori', cat.nomCategori)
        db.session.commit()
        return jsonify({'mesage':'categorie modifié avec succée'}),200
    
    if request.method == 'DELETE':
        db.session.delete(cat)
        db.session.commit()
        return jsonify ({'mesage': 'categorie supprimé avec succée'}),200

# admin recupere t evenement
@app.route('/api/admin/evenements', methods=['GET'])

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

("""
     # delete this===>214
    if request.method == 'POST':
        data = request.json
        cat = Categories.query.filter_by(nomCategori=data.get('categori')).first()
        if not cat:
            return jsonify({'erreur':'categorie pas trouvée'}),400
        
        new_evenement = Evenement(
            nomEvenement = data.get('nomEvenement'),
            typeEvenement = data.get('typeEvenement'),
            dateEvenement = data.get('dateEvenement'),
            PrixEvenement = data.get('PrixEvenement'),
            categorie = cat
        )
        db.session.add(new_evenement)
        db.session.commit()
        return jsonify({'mesage':'evenement crée avec succée'}),201
    """)


@app.route('/api/admin/evenements', methods=['POST'])

@jwt_required()
def ajout_evenement():
    data = request.json
    print("données reçues :", data)  # This is printing the incoming data

    #  verif si tout f.require sont présent
    champs_requis = ['nomEvenement', 'typeEvenement', 'dateEvenement', 'PrixEvenement', 'adresse', 'category_id']
    champs_manquants = [champ for champ in champs_requis if champ not in data or not data[champ]]

    if champs_manquants:
        print(f"Champs manquants: {', '.join(champs_manquants)}")  # Log the missing fields
        return jsonify({'erreur': f'champs manquants : {", ".join(champs_manquants)}'}), 400

    # Vérifier si la catégorie existe
    cat = Categories.query.get(data['category_id'])
    if not cat:
        print(f"Catégorie non trouvée pour l'ID {data['category_id']}")  # Log if category doesn't exist
        return jsonify({'erreur': 'Catégorie non trouvée'}), 404

    # Create the event
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


@app.route('/api/admin/evenements/<int:id>', methods=['PUT','DELETE'])

@jwt_required()

def mise_ajour_supprim_evenement(id):
    event = db.session.get(Evenement,id)
    if not event:
        return jsonify({'erreur':'evenement pas trouvée'}),404
    
    #modification evenement
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




   
if __name__=='__main__':
    app.run(debug=True)