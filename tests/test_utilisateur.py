import unittest
from app import app, db, utilisateur   

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        # Créer un admin
        if not utilisateur.query.filter_by(role='ADMIN').first():
            admin = utilisateur(
                nom='admin',
                email='admin@example.com',
                motPasse='adminpass',  
                role='ADMIN'
            )
            db.session.add(admin)
            db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

def test_ajouter_client(self):
    data = {
        "nomUtilisateur": "Test",
        "prenomUtilisateur": "Client",
        "email": "client@test.com",
        "motPasse": "password123",
        "role": "CLIENT"
    }

    response = self.app.post('/api/inscription', json=data)
    self.assertEqual(response.status_code, 201)
    self.assertIn(b'utilisateur cr\xc3\xa9e avec succ\xc3\xa8s', response.data)

    client = utilisateur.query.filter_by(email="client@test.com").first()
    self.assertIsNotNone(client)
    self.assertEqual(client.nomUtilisateur, "Test")

if __name__ == '__main__':
    unittest.main()
