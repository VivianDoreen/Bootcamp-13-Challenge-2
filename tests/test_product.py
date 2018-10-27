from flask import json
from tests.sample_data import MyTestCase

class TestProduct(MyTestCase):    
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Welcome to ManagerStore")
   
    def test_unavailable_fetch(self):
        result = self.client.get('/api/v1/products/')
        self.assertEqual(result.status_code, 404)

    # def test_empty_product_list(self):
    #     result = self.client.get('/api/v1/products')
    #     self.assertEqual(result.status_code, 200)
    #     self.assertEqual(json.loads(result.data.decode()), {'Product List': 'No products available'})
    
    def test_list_with_products(self):
        self.client.post('/api/v1/products',
                        content_type='application/json',
                        data=self.product
                        )
        result = self.client.get('/api/v1/products')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.data.decode()), {"Product List":[self.data_to_test]})
        self.client.delete('/api/v1/products/1')

    def test_get_single_product_that_does_not_exist(self):
        """ Should return product not found and status code 404"""
        self.client.post('/api/v1/products',
                         content_type='application/json',
                         data=self.product
                         )

        response = self.client.get('/api/v1/products/6')
        self.assertEqual({'product not found': 'please check id'}, json.loads(response.data.decode('utf8')))
        self.assertEqual(response.status_code, 404)
        self.client.delete('/api/v1/products/1')

    def test_single_product_successfully(self):
        self.client.post('/api/v1/products',
                        content_type='application/json',
                        data=self.product
                        )
        result = self.client.get('/api/v1/products/1')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.data.decode()), [self.data_to_test])
        self.client.delete('/api/v1/products/1')

    def test_add_null_value_for_product(self):
        """ Should return product not found, Wrong params for json"""
        response = self.client.post('/api/v1/products',
                                    content_type='application/json',
                                    data=self.null_value_product
                                    )
        self.assertEqual(
                        "Check your input values."
                        "\n Product_name*"
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
                        "\n\t\t\t\t- Must begin with a character"
            , response.data.decode())
        self.assertEqual(response.status_code, 422)
        self.client.delete('/api/v1/products/1')

    def test_add_product_without_some_params(self):
        """ Should return product not found, Wrong params for json"""
        response = self.client.post('/api/v1/products',
                                    content_type='application/json',
                                    data=self.product_with_missing_parameters
                                    )
        self.assertEqual({'product not found':'Wrong params for json'}, json.loads(response.data.decode()))
        self.assertEqual(response.status_code, 400)
        self.client.delete('/api/v1/products/1')
    
    def test_add_product_with_same_data(self):
        """ Should return missing or bad parameters"""
        self.client.post('/api/v1/products',
                                    content_type='application/json',
                                    data=self.product
                                    )
        response = self.client.post('/api/v1/products',
                                    content_type='application/json',
                                    data=self.product
                                    )
        self.assertEqual({'Message': 'Product already exists'}, json.loads(response.data.decode()))
        self.assertEqual(response.status_code, 409)
        self.client.delete('/api/v1/products/1')
    
    def test_add_product_successfully(self):
        post_product = self.client.post('/api/v1/products',
                                        content_type='application/json',
                                        data = self.product
                                        )
        self.assertEqual(post_product.status_code, 201)
        self.assertEqual(json.loads(post_product.data.decode()), {'message': 'Product successfully added'})
        self.client.delete('/api/v1/products/1')

    def test_update_product_that_does_not_exist(self):
        update_product = self.client.put('/api/v1/products/2', content_type='application/json', data =self.update_product)
        self.assertEqual(update_product.status_code, 404)
        self.assertEqual(json.loads(update_product.data.decode()), {'product not found': 'please check id'})
        self.client.delete('/api/v1/products/1')

    def test_update_product_successfully(self):
        self.client.post('/api/v1/products',
                         content_type='application/json',
                         data=self.product
                        )
        update_product = self.client.put('/api/v1/products/1', content_type='application/json', data = self.update_product)
        self.assertEqual(update_product.status_code, 201)
        self.assertEqual(json.loads(update_product.data.decode()), {'Message': 'Product has been modified successfully'})
        self.client.delete('/api/v1/products/1')

    def test_delete_product_that_does_not_exist(self):
        result = self.client.delete('/api/v1/products/2')
        self.assertEqual(result.status_code, 404)
        self.assertEqual(json.loads(result.data.decode()), {'product not found': 'please check id'})
        self.client.delete('/api/v1/products/2')

    def test_delete_product_successfully(self):
        self.client.post('/api/v1/products',
                        content_type='application/json',
                        data=self.product
                        )
        result = self.client.delete('/api/v1/products/1')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.data.decode()), {'Message': 'Product deleted'})
    
    
