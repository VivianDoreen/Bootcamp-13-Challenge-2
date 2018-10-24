import unittest
import json
from app.products import view
from app import app
from cerberus import Validator

class MyTestCase(unittest.TestCase):
    product={
             "product_name": "Nanuscripts books",
             "pdt_description":"Blue",
             "pdt_category":"Books"
            }
    null_value_product={
             "product_name": "",
             "pdt_description":"",
             "pdt_category":""
            }
    data_to_test = {
                 "date": "Wednesday.October.2018",
                 "pdt_category": "Books",
                 "pdt_description": "Blue",
                 "product_code": 1,
                 "product_name": "Nanuscripts books"
                }
    product_with_missing_parameters = {
                                        "date":"Fri, 28 Sep 2018 00:00:00 GMT",
                                        "product_code":2,
                                        "product_name":"Chairs" ,
                                        "pdt_description": "Blue"
                                        }
    update_product={
                    "product_name":"T-Shirts" ,
                    "pdt_description": "Blue",
                    "pdt_category": "Clothes"
                }

    def setUp(self):
        self.client = app.test_client()
    
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data.decode()), {"Hello Admin":"Welcome to ManagerStore"})
   
    def test_unavailable_fetch(self):
        result = self.client.get('/api/v1/products/')
        self.assertEqual(result.status_code, 404)

    def test_empty_product_list(self):
        result = self.client.get('/api/v1/products')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.data.decode()), {'200': 'No products available'})
    
    def test_list_with_products(self):
        self.client.post('/api/v1/products',
                        content_type='application/json',
                        data=json.dumps(self.product)
                        )
        result = self.client.get('/api/v1/products')
        print(result)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.data.decode()), {'200': [self.data_to_test]})
        self.client.delete('/api/v1/products/1')

    def test_get_single_product_that_does_not_exist(self):
        """ Should return product not found and status code 404"""
        result = self.client.post('/api/v1/products',
                         content_type='application/json',
                         data=json.dumps(self.product)
                         )

        response = self.client.get('/api/v1/products/6')
        self.assertEqual({'404': 'Product not found, please check id'}, json.loads(response.data.decode('utf8')))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result.status_code, 201)
        self.client.delete('/api/v1/products/1')

    def test_single_product_successfully(self):
        self.client.post('/api/v1/products',
                        content_type='application/json',
                        data=json.dumps(self.product)
                        )
        result = self.client.get('/api/v1/products/1')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.data.decode()), [self.data_to_test])
        self.client.delete('/api/v1/products/1')

    def test_add_null_value_for_product(self):
        """ Should return product not found, Wrong params for json"""
        response = self.client.post('/api/v1/products',
                                    content_type='application/json',
                                    data=json.dumps(self.null_value_product)
                                    )
        self.assertEqual("Check your input values."
                    "\n Product_name*:, "
                    " \n\t\t\t\t- Required"
                    "\n\t\t\t\t- Must be a string, "
                    "\n\t\t\t\t- Minlength: 2 characters"
                    "\n\t\t\t\t- Must begin with a character"
                    "\n Pdt_description*"
                    "\n\t\t\t\t- Required"
                    "\n\t\t\t\t- Must be a string"
                    "\n\t\t\t\t- Minlength : 2 characters"
                    "\n\t\t\t\t- Must begin with a character"
                    "\n -Pdt_category* "
                    "\n\t\t\t\t- Required"
                    "\n\t\t\t\t- Must be a string "
                    "\n\t\t\t\t- Minlength : 2 characters"
                    "\n\t\t\t\t- Must begin with a character", response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.client.delete('/api/v1/products/1')

    def test_add_product_without_some_params(self):
        """ Should return product not found, Wrong params for json"""
        response = self.client.post('/api/v1/products',
                                    content_type='application/json',
                                    data=json.dumps(self.product_with_missing_parameters)
                                    )
        self.assertEqual({'product not found':' Wrong params for json'}, json.loads(response.data.decode()))
        self.assertEqual(response.status_code, 400)
        self.client.delete('/api/v1/products/1')
    
    def test_add_product_with_same_data(self):
        """ Should return missing or bad parameters"""
        self.client.post('/api/v1/products',
                                    content_type='application/json',
                                    data=json.dumps(self.product)
                                    )
        response = self.client.post('/api/v1/products',
                                    content_type='application/json',
                                    data=json.dumps(self.product)
                                    )
        self.assertEqual({'403': 'Product already exists'}, json.loads(response.data.decode()))
        self.assertEqual(response.status_code, 403)
        self.client.delete('/api/v1/products/1')
    
    def test_add_product_successfully(self):
        post_product = self.client.post('/api/v1/products',
                                        content_type='application/json',
                                        data = json.dumps(self.product)
                                        )
        self.assertEqual(post_product.status_code, 201)
        self.assertEqual(json.loads(post_product.data.decode()), {'201': 'Product successfully added'})
        self.client.delete('/api/v1/products/1')

    def test_update_product_that_does_not_exist(self):
        self.client.post('/api/v1/products',
                        content_type='application/json',
                        data=json.dumps(self.product)
                        )

        update_product = self.client.put('/api/v1/products/2', content_type='application/json', data = json.dumps(self.update_product))
        self.assertEqual(update_product.status_code, 404)
        self.assertEqual(json.loads(update_product.data.decode()), {'404': 'Product not found, please check id'})
        self.client.delete('/api/v1/products/1')

    def test_update_product_successfully(self):
        self.client.post('/api/v1/products',
                         content_type='application/json',
                         data=json.dumps(self.product)
                        )
        update_product = self.client.put('/api/v1/products/1', content_type='application/json', data = json.dumps(self.update_product))
        self.assertEqual(update_product.status_code, 201)
        self.assertEqual(json.loads(update_product.data.decode()), {'201': 'Product has been modified successfully'})
        self.client.delete('/api/v1/products/1')

    def test_delete_product_that_does_not_exist(self):
        self.client.post('/api/v1/products',
                        content_type='application/json',
                        data=json.dumps(self.product)
                        )
        result = self.client.delete('/api/v1/products/2')
        self.assertEqual(result.status_code, 404)
        self.assertEqual(json.loads(result.data.decode()), {'404': 'Product not found, please check id'})
        self.client.delete('/api/v1/products/1')

    def test_delete_product_successfully(self):
        self.client.post('/api/v1/products',
                        content_type='application/json',
                        data=json.dumps(self.product)
                        )
        result = self.client.delete('/api/v1/products/1')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.data.decode()), {'200': 'Product deleted'})
    
    
