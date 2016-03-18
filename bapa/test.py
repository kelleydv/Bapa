"""
Base class for tests in modules.
"""

from bapa import app, db
import unittest

class BaseTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db
        self.db.session.close()
        self.db.drop_all()
        self.db.create_all()

    def tearDown(self):
        pass


    def register(self, **kwargs):
        return self.app.post('/register', data=kwargs, follow_redirects=True)

    def login(self, **kwargs):
        return self.app.post('/login', data=kwargs, follow_redirects=True)
