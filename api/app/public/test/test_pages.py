import unittest

from app.auth.models import User
from . import BaseTestClass


class AuthUserTest(BaseTestClass):

    def test_index(self):
        res = self.client.get('/')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'Wanacare', res.data)
'''
    def test_redirect_to_login(self):
        res = self.client.get('/protect')
        self.assertEqual(302, res.status_code)
        self.assertIn(b'Redirecting...', res.data)

    def test_unauthorized_access_to_admin(self):
        self.login('guest@xyz.com', '1111')
        res = self.client.get('/home')
        self.assertEqual(401, res.status_code)
        #self.assertIn(b'Ooops!! No tienes permisos de acceso', res.data)

    def test_authorized_access_to_admin(self):
        self.login('admin@xyz.com', '1111')
        res = self.client.get('/fome')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'Posts', res.data)
        self.assertIn(b'Usuarios', res.data)

'''
if __name__ == '__main__':
    unittest.main()