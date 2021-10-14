#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from myapp import app, db
from myapp.models import Order



import os
import json
import unittest
import tempfile

from hamcrest import *

class OrdersTestCase(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)
        app.config['TESTING'] = True
        
    def tearDown(self):
        Order.query.delete()
        db.session.commit()
        del self.tester


    def _add_test_order(self):
        dict_order = {  
                            "shippingPlace":"town1", 
                            "customer":"someone", 
                            "price":"12", 
                            "duration":"12", 
                            "weight":"30"}

        return self.tester.post('/orders', content_type='application/json', json=dict_order)

    def test_get_empty(self):
        response= self.tester.get('/orders', content_type='application/json')
        self.assertEqual(json.loads(response.data.decode("utf-8")), {'orders':[]})
        self.assertEqual(response.status_code, 200)

        
    def test_get_order(self):
        response= self._add_test_order()
        response= self.tester.get('/orders/dG93bjFzb21lb25lMTIxMjMw', content_type='application/json')
        assert_that(response.data.decode("utf-8"), contains_string('town1'))
        self.assertEqual(response.status_code, 200)

        
    def test_get_order_not_found(self):
        response= self.tester.get('/orders/NONE', content_type='application/json')
        self.assertEqual(response.status_code, 404)
        

    def test_add_order_error(self):
        response= self.tester.post('/orders', content_type='application/json', data=json.dumps({'name':'a1'}))
        self.assertEqual(response.status_code, 400)

    

    def test_add_order(self):
        response= self._add_test_order()
        self.assertEqual(json.loads(response.data.decode("utf-8")), {'created':'dG93bjFzb21lb25lMTIxMjMw'})
        self.assertEqual(response.status_code, 201)


    def test_add_order_conflict(self):
        response1=self._add_test_order()
        response2=self._add_test_order()
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 409)
        

    def test_get_orders(self):
        self._add_test_order()
        response=self.tester.get('/orders', content_type='application/json')
        assert_that(response.data.decode("utf-8"), contains_string('town1'))
        self.assertEqual(response.status_code, 200)


    def test_delete_not_order_found(self):
        response=self.tester.delete('/orders/NONE', content_type='application/json')        
        self.assertEqual(response.status_code, 404)


    def test_delete_order(self):
        responsePost = self._add_test_order()
        code = json.loads(responsePost.data.decode("utf-8"))['created']
        response=self.tester.delete('/orders/'+code, content_type='application/json')        
        self.assertEqual(json.loads(response.data.decode("utf-8")), {'deleted':str(code)})
        self.assertEqual(response.status_code, 200)
    
        
        
if __name__ == '__main__':
    unittest.main()
 
 
