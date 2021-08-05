import unittest

from app.auth.models import User
from . import BaseTestClass


class ChangePasswordTest(BaseTestClass):

def test_change_password_page(self):
    self.app.get('/register', follow_redirects=True)
    self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
    response = self.app.get('/password_change')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Password Change', response.data)
 
def test_change_password(self):
    self.app.get('/register', follow_redirects=True)
    self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
    response = self.app.post('/password_change', data=dict(password='MyNewPassword1234'), follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Password has been updated!', response.data)
    self.assertIn(b'User Profile', response.data)
 
def test_change_password_logging_in(self):
    response = self.app.get('/password_change')
    self.assertEqual(response.status_code, 302)
    self.assertIn(b'You should be redirected automatically to target URL:', response.data)
    self.assertIn(b'/login?next=%2Fpassword_change', response.data)
    response = self.app.post('/password_change', data=dict(password='MyNewPassword1234'), follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Log In', response.data)
    self.assertIn(b'Need an account?', response.data)