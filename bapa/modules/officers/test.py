from bapa.test import BaseTest
from bapa.models import Officer, User
import unittest
import os

class OfficersTestCase(BaseTest):

    def test_appointment(self):

        #redirect to the signin page
        resp = self.app.get('/officers', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Sign In' in resp.data)

        #register two users
        self.register(ushpa='12345', email='johndoe@example.com',
                                password='pass', password2='pass',
                                firstname='John', lastname='Doe')
        self.register(ushpa='98765', email='janedoe@example.com',
                                password='pass', password2='pass',
                                firstname='Jane', lastname='Doe')

        john = User.query.filter_by(ushpa='12345').first()
        jane = User.query.filter_by(ushpa='98765').first()

        #login john
        self.login(ushpa='12345', password='pass')

        #redirect to the home page, (no officer permissions)
        resp = self.app.get('/officers', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Take Flight' in resp.data)
        officers = Officer.query.all()
        self.assertEqual(len(officers), 0)

        #attempt to appoint another as an officer, get redirected
        resp = self.app.get(
            '/officers/appoint',
            query_string = dict(user_id=jane.id),
            follow_redirects = True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Take Flight' in resp.data)
        officers = Officer.query.all()
        self.assertEqual(len(officers), 0)

        #self-appointment as an officer
        key = os.environ['APPOINTMENT_KEY'] = 'abcd'
        #wrong key
        self.app.get('/officers/appoint/%s' % 'zyxw', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        #self.assertTrue(b'failed' in resp.data)
        #correct key
        self.app.get('/officers/appoint/%s' % key, follow_redirects=True)
        officers = Officer.query.all()
        self.assertEqual(len(officers), 1)
        resp = self.app.get('/officers', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Members' in resp.data)

        #appoint another officer
        self.app.get(
            '/officers/appoint',
            query_string = dict(user_id=jane.id),
            follow_redirects = True
        )
        officers = Officer.query.all()
        self.assertEqual(len(officers), 2)

        del os.environ['APPOINTMENT_KEY']
