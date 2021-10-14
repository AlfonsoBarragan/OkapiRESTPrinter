#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from myapp import app, db
from myapp.models import Filament



import os
import json
import unittest
import tempfile

from hamcrest import *

class FilamentsTestCase(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)
        app.config['TESTING'] = True
        
    def tearDown(self):
        Filament.query.delete()
        db.session.commit()
        del self.tester


    def _add_test_filament(self):
        dict_filament = {  
                            "name":"filament1", 
                            "seller":"someone", 
                            "link":"online-shop.com", 
                            "price":"16.50", 
                            "weight":"1",
                            "width":"1.75"}

        return self.tester.post('/filaments', content_type='application/json', json=dict_filament)

    def test_get_empty(self):
        response= self.tester.get('/filaments', content_type='application/json')
        self.assertEqual(json.loads(response.data.decode("utf-8")), {'filaments':[]})
        self.assertEqual(response.status_code, 200)

        
    def test_get_filament(self):
        response= self._add_test_filament()
        response= self.tester.get('/filaments/ZmlsYW1lbnQxc29tZW9uZW9ubGluZS1zaG9wLmNvbTE2LjUwMTEuNzU=', content_type='application/json')
        assert_that(response.data.decode("utf-8"), contains_string('filament1'))
        self.assertEqual(response.status_code, 200)

        
    def test_get_filament_not_found(self):
        response= self.tester.get('/filaments/NONE', content_type='application/json')
        self.assertEqual(response.status_code, 404)
        

    def test_add_filament_error(self):
        response= self.tester.post('/filaments', content_type='application/json', data=json.dumps({'name':'a1'}))
        self.assertEqual(response.status_code, 400)

    

    def test_add_filament(self):
        response= self._add_test_filament()
        self.assertEqual(json.loads(response.data.decode("utf-8")), {'created':'ZmlsYW1lbnQxc29tZW9uZW9ubGluZS1zaG9wLmNvbTE2LjUwMTEuNzU='})
        self.assertEqual(response.status_code, 201)


    def test_add_filament_conflict(self):
        response1=self._add_test_filament()
        response2=self._add_test_filament()
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 409)
        

    def test_get_filaments(self):
        self._add_test_filament()
        response=self.tester.get('/filaments', content_type='application/json')
        assert_that(response.data.decode("utf-8"), contains_string('filament1'))
        self.assertEqual(response.status_code, 200)


    def test_delete_not_filament_found(self):
        response=self.tester.delete('/filaments/NONE', content_type='application/json')        
        self.assertEqual(response.status_code, 404)


    def test_delete_filament(self):
        responsePost = self._add_test_filament()
        code = json.loads(responsePost.data.decode("utf-8"))['created']
        response=self.tester.delete('/filaments/'+code, content_type='application/json')        
        self.assertEqual(json.loads(response.data.decode("utf-8")), {'deleted':str(code)})
        self.assertEqual(response.status_code, 200)
    
        
        
if __name__ == '__main__':
    unittest.main()
 
 
