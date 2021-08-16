import unittest
from app import create_app, db


class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        # Crea un contexto de aplicación
        with self.app.app_context():
            # Crea las tablas de la base de datos
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            db.session.remove()
            db.drop_all()
