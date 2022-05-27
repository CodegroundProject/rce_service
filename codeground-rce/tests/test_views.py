import json
import os
import unittest
from app.app import MyMicroservice
from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT
from typing import Dict, List, Union, Text


class AppTestCase(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(
            self.BASE_DIR, "config-tests.yml")
        ms = MyMicroservice(path=os.path.join(os.path.dirname(
            os.path.dirname(__file__)), "project", "test_views.py"))
        self.app = ms.create_app()
        self.base_url = self.app.config["APPLICATION_ROOT"]
        self.client = self.app.test_client()

    def tearDown(self):
        pass  # os.unlink(self.app.config['DATABASE'])

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(404, response.status_code)

    def test_healthcheck(self):
        response = self.client.get('/healthcheck')
        self.assertEqual(200, response.status_code)

    def test_list_view(self):
        response = self.client.get('/python_microservices_boilerplate/')
        self.assertEqual(200, response.status_code)

    def test_create_view(self):
        name = "blue"
        response = self.client.post('/python_microservices_boilerplate/',
                                    data=json.dumps(dict(name=name)),
                                    content_type='application/json'
                                    )
        self.assertEqual(200, response.status_code)
