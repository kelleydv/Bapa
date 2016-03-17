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
