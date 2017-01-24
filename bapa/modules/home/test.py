from bapa.test import BaseTest
from bapa.models import ResetPassword
import unittest

class HomeTestCase(BaseTest):

    def test_home_page(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Take Flight' in resp.data)

    def test_registration(self):
        resp = self.app.get('/register')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Register' in resp.data)
        resp = self.register(ushpa='12345', email='johndoe@example.com',
                        password='pass', password2='pass',
                        firstname='John', lastname='Doe')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'successfully' in resp.data)

    def test_login(self):
        resp = self.app.get('/login')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Login' in resp.data)
        self.register(ushpa='12345', email='johnDoe@example.com',
                        password='pass', password2='pass',
                        firstname='John', lastname='Doe')

        ##Login with ushpa number
        #bad password
        resp = self.login(ushpa_or_email='12345', password='mass')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Error' in resp.data)

        #bad ushpa number
        resp = self.login(ushpa_or_email='12346', password='pass')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Error' in resp.data)

        #good login
        resp = self.login(ushpa_or_email='12345', password='pass')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Welcome back' in resp.data)


        self.app.get('/logout')
        ##Login with email
        #bad password
        resp = self.login(ushpa_or_email='johndoe@example.com', password='mass')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Error' in resp.data)

        #bad email
        resp = self.login(ushpa_or_email='johndoe@example.org', password='pass')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Error' in resp.data)

        #good login
        resp = self.login(ushpa_or_email='johndoe@example.com', password='pass')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Welcome back' in resp.data)

        #redirect authed user
        resp = self.app.get('/login', follow_redirects=True)
        self.assertFalse(b'Login' in resp.data)
        self.assertTrue(b'Home' in resp.data)

    def test_logout(self):
        self.register(ushpa='12345', email='johndoe@example.com',
                        password='pass', password2='pass',
                        firstname='John', lastname='Doe')
        self.login(ushpa='12345', password='pass')
        resp = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Home' in resp.data)
        self.assertTrue(b'logged out' in resp.data)

    def test_password_reset(self):
        self.register(ushpa='12345', email='johndoe@example.com',
                        password='pass', password2='pass',
                        firstname='John', lastname='Doe')

        resp = self.app.get('/password/reset/request')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Reset Password' in resp.data)


        #wrong email
        resp = self.app.post(
            '/password/reset/request',
            data = dict(ushpa_or_email='johndoe@example.org'),
            follow_redirects = True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Email sent' in resp.data)
        self.assertTrue(b'Home' in resp.data)
        reset = ResetPassword.query.all()
        self.assertEqual(len(reset), 0)

        #wrong ushpa
        resp = self.app.post(
            '/password/reset/request',
            data = dict(ushpa_or_email='12346'),
            follow_redirects = True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Email sent' in resp.data)
        self.assertTrue(b'Home' in resp.data)
        reset = ResetPassword.query.all()
        self.assertEqual(len(reset), 0)

        #valid request for reset token, with email
        resp = self.app.post(
            '/password/reset/request',
            data = dict(ushpa_or_email='johndoe@example.com'),
            follow_redirects = True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Email sent' in resp.data)
        self.assertTrue(b'Home' in resp.data)
        resets = ResetPassword.query.all()
        self.assertEqual(len(resets), 1) #token exists
        resp = self.app.get('/password/reset/auth/%s' % resets[0].token)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Reenter Credentials' in resp.data)
        resp = self.app.post( #use token
            '/password/reset/auth/%s' % resets[0].token,
            data = dict(ushpa_or_email='johndoe@example.com'),
            follow_redirects = True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'New Password' in resp.data)
        resets = ResetPassword.query.all()
        self.assertEqual(len(resets), 0)
        resp = self.app.post( #new password
            '/password/reset',
            data = dict(password='password', password2='password'),
            follow_redirects = True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'has been reset' in resp.data)
        resp = self.login(ushpa_or_email='12345', password='pass') #old password
        self.assertTrue(b'Error' in resp.data)
        resp = self.login(ushpa_or_email='12345', password='password') #new password
        self.assertTrue(b'Welcome back' in resp.data)

        self.app.get('/logout')
        #valid request for reset token, with ushpa
        resp = self.app.post(
            '/password/reset/request',
            data = dict(ushpa_or_email='12345'),
            follow_redirects = True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Email sent' in resp.data)
        self.assertTrue(b'Home' in resp.data)
        resets = ResetPassword.query.all()
        self.assertEqual(len(resets), 1) #token exists
        resp = self.app.get('/password/reset/auth/%s' % resets[0].token)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Reenter Credentials' in resp.data)
        resp = self.app.post( #use token
            '/password/reset/auth/%s' % resets[0].token,
            data = dict(ushpa_or_email='12345'),
            follow_redirects = True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'New Password' in resp.data)
        resets = ResetPassword.query.all()
        self.assertEqual(len(resets), 0)
        resp = self.app.post( #new password
            '/password/reset',
            data = dict(password='password123', password2='password123'),
            follow_redirects = True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'has been reset' in resp.data)
        resp = self.login(ushpa_or_email='12345', password='password') #old password
        self.assertTrue(b'Error' in resp.data)
        resp = self.login(ushpa_or_email='12345', password='password123') #new password
        self.assertTrue(b'Welcome back' in resp.data)



if __name__ == '__main__':
    unittest.main(verbosity=2)
