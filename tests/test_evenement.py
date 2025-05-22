import unittest
import json
from app import app, db
from modeles.modele import Categories, utilisateur
from werkzeug.security import generate_password_hash

class EvenementTestCase(unittest.TestCase):

    def setUp(self):
        # Configuration de teste
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests/test_db.sqlite' 
        app.config['TESTING'] = True
        self.app = app.test_client()  

        with app.app_context():
            db.create_all()  # Crée les tables 

            # Ajouter une catégorie 
            category = Categories.query.first()
            if not category:
                category = Categories(nomCategori='Concert')
                db.session.add(category)
                db.session.commit()
            self.category_id = category.id

            # Ajouter un utilisateur admin 
            existing_admin = utilisateur.query.filter_by(email="admin@admin.com").first()
            if not existing_admin:
                admin_user = utilisateur(
                    nomUtilisateur="Admin",
                    prenomUtilisateur="User",
                    email="admin@admin.com",
                    motPasse=generate_password_hash("admin789"),
                    role='admin'
                )
                db.session.add(admin_user)
                db.session.commit()

            # Connexion pour récupérer le token JWT
            response = self.app.post(
                '/api/connexion',
                data=json.dumps({
                    "email": "admin@admin.com",
                    "motPasse": "admin789"
                }),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200, "Échec de la connexion lors du setUp")
            data = json.loads(response.data)
            self.token = data.get('access_token')
            self.assertIsNotNone(self.token, "Token JWT non reçu")

    def tearDown(self):
        with app.app_context():
            db.session.remove()

    def auth_header(self):
        return {'Authorization': f'Bearer {self.token}'}

    def test_ajout_evenement_success(self):
        payload = {
            "nomEvenement": "Test Event",
            "typeEvenement": "foot",
            "dateEvenement": "2025-12-31",
            "PrixEvenement": 100,
            "adresse": "123 Test ",
            "category_id": self.category_id
        }
        response = self.app.post(
            '/api/admin/evenements',
            data=json.dumps(payload),
            content_type='application/json',
            headers=self.auth_header()
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data.get('message'), 'Événement créé avec succès')

    def test_ajout_evenement_missing_fields(self):
        payload = {
            "typeEvenement": "hand",
            "dateEvenement": "2025-12-31",
            "PrixEvenement": 100,
            "adresse": "123 Test ",
            "category_id": self.category_id
        }
        response = self.app.post(
            '/api/admin/evenements',
            data=json.dumps(payload),
            content_type='application/json',
            headers=self.auth_header()
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('erreur', data)
        self.assertIn('nomEvenement', data['erreur'])

    def test_ajout_evenement_category_not_found(self):
        payload = {
            "nomEvenement": "Test Event",
            "typeEvenement": "foot",
            "dateEvenement": "2025-12-31",
            "PrixEvenement": 100,
            "adresse": "123 Test ",
            "category_id": 9999  # Catégorie inexistante
        }
        response = self.app.post(
            '/api/admin/evenements',
            data=json.dumps(payload),
            content_type='application/json',
            headers=self.auth_header()
        )
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data.get('erreur'), 'Catégorie non trouvée')

if __name__ == '__main__':
    unittest.main()
