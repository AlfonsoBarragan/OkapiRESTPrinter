#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from myapp import app, db
from myapp.models import Printer



import os
import json
import unittest
import tempfile

from hamcrest import *

class PrintersTestCase(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)
        app.config['TESTING'] = True
        
    def tearDown(self):
        Printer.query.delete()
        db.session.commit()
        del self.tester


    def _add_test_printer(self):
        dict_printer = {  
                            "name":"printer1", 
                            "consume":"500"}

        return self.tester.post('/printers', content_type='application/json', json=dict_printer)

    def test_get_empty(self):
        response= self.tester.get('/printers', content_type='application/json')
        self.assertEqual(json.loads(response.data.decode("utf-8")), {'printers':[]})
        self.assertEqual(response.status_code, 200)

        
    def test_get_printer(self):
        response= self._add_test_printer()
        response= self.tester.get('/printers/cHJpbnRlcjE1MDA=', content_type='application/json')
        assert_that(response.data.decode("utf-8"), contains_string('printer1'))
        self.assertEqual(response.status_code, 200)

        
    def test_get_printer_not_found(self):
        response= self.tester.get('/printers/NONE', content_type='application/json')
        self.assertEqual(response.status_code, 404)
        

    def test_add_printer_error(self):
        response= self.tester.post('/printers', content_type='application/json', data=json.dumps({'name':'a1'}))
        self.assertEqual(response.status_code, 400)

    

    def test_add_printer(self):
        response= self._add_test_printer()
        self.assertEqual(json.loads(response.data.decode("utf-8")), {'created':'cHJpbnRlcjE1MDA='})
        self.assertEqual(response.status_code, 201)


    def test_add_printer_conflict(self):
        response1=self._add_test_printer()
        response2=self._add_test_printer()
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 409)
        

    def test_get_printers(self):
        self._add_test_printer()
        response=self.tester.get('/printers', content_type='application/json')
        assert_that(response.data.decode("utf-8"), contains_string('printer1'))
        self.assertEqual(response.status_code, 200)


    def test_delete_not_printer_found(self):
        response=self.tester.delete('/printers/NONE', content_type='application/json')        
        self.assertEqual(response.status_code, 404)


    def test_delete_printer(self):
        responsePost = self._add_test_printer()
        code = json.loads(responsePost.data.decode("utf-8"))['created']
        response=self.tester.delete('/printers/'+code, content_type='application/json')        
        self.assertEqual(json.loads(response.data.decode("utf-8")), {'deleted':str(code)})
        self.assertEqual(response.status_code, 200)
    
 
if __name__ == '__main__':
    unittest.main()
 
 
