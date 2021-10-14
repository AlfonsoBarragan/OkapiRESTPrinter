#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from myapp import app, db
from myapp.models import Creation



import os
import json
import unittest
import tempfile

from hamcrest import *

class CreationsTestCase(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)
        app.config['TESTING'] = True
        
    def tearDown(self):
        Creation.query.delete()
        db.session.commit()
        del self.tester


    def _add_test_creation(self):
        dict_creation = {  
                            "name":"cosa", 
                            "author":"yo", 
                            "price":"12", 
                            "time":"12", 
                            "materialWasted":"30",
                            "description":"Mediocre"}

        return self.tester.post('/creations_printed', content_type='application/json', json=dict_creation)

    def test_get_empty(self):
        response= self.tester.get('/creations_printed', content_type='application/json')
        self.assertEqual(json.loads(response.data.decode("utf-8")), {'creations':[]})
        self.assertEqual(response.status_code, 200)

        
    def test_get_creation(self):
        response= self._add_test_creation()
        response= self.tester.get('/creations_printed/Y29zYXlvMTIxMjMw', content_type='application/json')
        assert_that(response.data.decode("utf-8"), contains_string('cosa'))
        self.assertEqual(response.status_code, 200)

        
    def test_get_creation_not_found(self):
        response= self.tester.get('/creations_printed/NONE', content_type='application/json')
        self.assertEqual(response.status_code, 404)
        

    def test_add_creation_error(self):
        response= self.tester.post('/creations_printed', content_type='application/json', data=json.dumps({'name':'a1'}))
        self.assertEqual(response.status_code, 400)

    

    def test_add_creation(self):
        response= self._add_test_creation()
        self.assertEqual(json.loads(response.data.decode("utf-8")), {'created':'Y29zYXlvMTIxMjMw'})
        self.assertEqual(response.status_code, 201)


    def test_add_creation_conflict(self):
        response1=self._add_test_creation()
        response2=self._add_test_creation()
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 409)
        

    def test_get_creations(self):
        self._add_test_creation()
        response=self.tester.get('/creations_printed', content_type='application/json')
        assert_that(response.data.decode("utf-8"), contains_string('cosa'))
        self.assertEqual(response.status_code, 200)


    def test_delete_not_creation_found(self):
        response=self.tester.delete('/creations_printed/NONE', content_type='application/json')        
        self.assertEqual(response.status_code, 404)


    def test_delete_creation(self):
        responsePost = self._add_test_creation()
        code = json.loads(responsePost.data.decode("utf-8"))['created']
        response=self.tester.delete('/creations_printed/'+code, content_type='application/json')        
        self.assertEqual(json.loads(response.data.decode("utf-8")), {'deleted':str(code)})
        self.assertEqual(response.status_code, 200)
    
        
        
if __name__ == '__main__':
    unittest.main()
 
