import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort, jsonify

from app import create_app
from models import setup_db, Project, Team
from auth.auth import AuthError, INT_TOKEN, EMP_TOKEN, SUP_TOKEN


class InnoTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "inno_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_projects(self):
        res = self.client().get('/projects')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['projects'])

    def test_get_project_detail(self):
        res = self.client().get('/projects/1/details')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.assertTrue(data['project'])

    def test_get_project_detail_fail(self):
        res = self.client().get('/projects/100/details')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_members(self):
        res = self.client().get(
            '/members',
            headers={"Authorization": "Bearer {}".format(SUP_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['members'])
        self.assertTrue(data['total_members'])

    # no permission
    def test_get_members_fail(self):
        res = self.client().get(
            '/members',
            headers={"Authorization": "Bearer {}".format(INT_TOKEN)})
        data = json.loads(res.data)

        # self.assertEqual(res.status_code, 403)
        self.assertEqual(data[1], 403)
        self.assertEqual(data[0]['success'], False)
        self.assertEqual(data[0]['message'], 'Permission not found')

    def test_add_project(self):
        res = self.client().post('/projects',
                                 data='{"title":"New Project",\
                                        "startDate":"2020-05-02",\
                                        "endDate":"2020-06-02",\
                                        "description":"this is a new project",\
                                        "completed":false}',
                                 headers={"Content-Type": "application/json",
                                          "Authorization":
                                          "Bearer {}".format(SUP_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.assertTrue(data['title'])
        self.assertTrue(data['project_created'])
        self.assertTrue(data['project_end'])
        self.assertTrue(data['description'])
        self.assertEqual(data['completed'], False)

    def test_add_project_fail(self):
        res = self.client().post('/projects',
                                 data='{"title":"New Project",\
                                        "startDate":"2020-05-02",\
                                        "endDate":"2020-06-02",\
                                        "description":"this is a new project",\
                                        "completed":false}',
                                 headers={"Content-Type": "application/json",
                                          "Authorization":
                                          "Bearer {}".format(INT_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(data[1], 403)
        self.assertEqual(data[0]['success'], False)
        self.assertEqual(data[0]['message'], 'Permission not found')

    def test_edit_project(self):
        res = self.client().patch('/projects/3',
                                  data='{"endDate":"2020-06-02",\
                                        "description":"this is a new project",\
                                        "completed":true}',
                                  headers={"Content-Type": "application/json",
                                           "Authorization":
                                           "Bearer {}".format(SUP_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['project_end'])
        self.assertTrue(data['description'])
        self.assertEqual(data['completed'], True)

    def test_edit_project_fail(self):
        res = self.client().patch('/projects/3',
                                  data='{"endDate":"2020-06-02",\
                                        "description":"this is a new project",\
                                        "completed":true}',
                                  headers={"Content-Type": "application/json",
                                           "Authorization":
                                           "Bearer {}".format(INT_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(data[1], 403)
        self.assertEqual(data[0]['success'], False)
        self.assertEqual(data[0]['message'], 'Permission not found')

    def test_delete_project(self):
        res = self.client().delete(
            '/projects/10',
            headers={"Authorization": "Bearer {}".format(SUP_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_project_fail(self):
        res = self.client().delete(
            '/projects/10',
            headers={"Authorization": "Bearer {}".format(INT_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(data[1], 403)
        self.assertEqual(data[0]['success'], False)
        self.assertEqual(data[0]['message'], 'Permission not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
