import unittest
import json
from app.sales import view
from app import app

class MyTestCase(unittest.TestCase):
    sale={
            "date": 'Wednesday.October.2018',
            "sales_id":1,
            "product_code" : 12333,
            "product_name" : "Cups",
            "unit_measure" : "pieces",
            "quantity" : 2,
            "unit_price" : 2000,
            "total_price" : 70000
        }
    all_list = [{
                "date": 'Wednesday.October.2018',
                "sales_id":1,
                "product_code" : 12333,
                "product_name" : "Cups",
                "unit_measure" : "pieces",
                "quantity" : 2,
                "unit_price" : 2000,
                "total_price" : 70000
                }]
    sale_with_missing_parameters={
                                  "product_name" : "Cups",
                                  "unit_measure" : "pieces",
                                  "quantity" : 2,
                                  "unit_price" : 2000,
                                  "total_price" : 70000
                                }
    update_sale = {
                   "product_code" : 12333,
                    "product_name" : "Cups",
                    "unit_measure" : "pieces",
                    "quantity" : 2,
                    "unit_price" : 2000,
                    "total_price" : 70000
                    }
    
    def setUp(self):
        self.client = app.test_client()
    
    def test_unavailable_fetch(self):
        result = self.client.get('/api/v1/sales/')
        self.assertEqual(result.status_code, 404)

    def test_empty_product_list(self):
        result = self.client.get('/api/v1/sales')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.data.decode()), {'200': 'No Sales available'})

    def test_list_with_sales(self):
        self.client.post('/api/v1/sales',
                        content_type='application/json',
                        data=json.dumps(self.sale)
                        )
        result = self.client.get('/api/v1/sales')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.data.decode()), {'200': self.all_list})
        self.client.delete('/api/v1/sales/1')

    def test_get_single_sales_that_does_not_exist(self):
        """ Should return sales not found and status code 404"""
        result = self.client.post('/api/v1/sales',
                         content_type='application/json',
                         data=json.dumps(self.sale)
                         )

        response = self.client.get('/api/v1/sales/6')
        self.assertEqual({'404': 'Sale not found, please check id'}, json.loads(response.data.decode('utf8')))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result.status_code, 201)
        self.client.delete('/api/v1/sales/1')

    def test_single_sale_successfully(self):
        self.client.post('/api/v1/sales',
                        content_type='application/json',
                        data=json.dumps(self.sale)
                        )
        result = self.client.get('/api/v1/sales/1')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.data.decode()), [self.sale])
        self.client.delete('/api/v1/sales/1')

    def test_add_sale_without_some_params(self):
        """ Should return sale not found, Wrong params for json"""
        response = self.client.post('/api/v1/sales',
                                    content_type='application/json',
                                    data=json.dumps(self.sale_with_missing_parameters)
                                    )
        self.assertEqual({'product not found':' Wrong params for json'}, json.loads(response.data.decode()))
        self.assertEqual(response.status_code, 400)
        self.client.delete('/api/v1/sales/1')

    def test_add_sale_with_same_data(self):
        """ Should return"""
        self.client.post('/api/v1/sales',
                                    content_type='application/json',
                                    data=json.dumps(self.sale)
                                    )
        response = self.client.post('/api/v1/sales',
                                    content_type='application/json',
                                    data=json.dumps(self.sale)
                                    )
        self.assertEqual({'403': 'Sale already exists'}, json.loads(response.data.decode()))
        self.assertEqual(response.status_code, 403)
        self.client.delete('/api/v1/sales/1')

    def test_add_sale_successfully(self):
        post_sale = self.client.post('/api/v1/sales',
                                        content_type='application/json',
                                        data = json.dumps(self.sale)
                                        )
        self.assertEqual(post_sale.status_code, 201)
        self.assertEqual(json.loads(post_sale.data.decode()), {'201': 'Sale successfully added'})
        self.client.delete('/api/v1/sales/1')

    def test_update_sale_that_does_not_exist(self):
        self.client.post('/api/v1/sales',
                        content_type='application/json',
                        data=json.dumps(self.sale)
                        )
        update_sale = self.client.put('/api/v1/sales/2', content_type='application/json', data = json.dumps(self.update_sale))
        self.assertEqual(update_sale.status_code, 404)
        self.assertEqual(json.loads(update_sale.data.decode()), {'404': 'Sale not found, please check id'})
        self.client.delete('/api/v1/sales/1')
    
    def test_update_sale_successfully(self):
        self.client.post('/api/v1/sales',
                         content_type='application/json',
                         data=json.dumps(self.sale)
                        )
        update_sale = self.client.put('/api/v1/sales/1', content_type='application/json', data = json.dumps(self.update_sale))
        self.assertEqual(update_sale.status_code, 201)
        self.assertEqual(json.loads(update_sale.data.decode()), {'201': 'Sale has been modified successfully'})
        self.client.delete('/api/v1/sales/1')
    
    def test_delete_sale_that_does_not_exist(self):
        self.client.post('/api/v1/sales',
                        content_type='application/json',
                        data=json.dumps(self.sale)
                        )
        result = self.client.delete('/api/v1/sales/2')
        self.assertEqual(result.status_code, 404)
        self.assertEqual(json.loads(result.data.decode()), {'404': 'Sale not found, please check id'})
        self.client.delete('/api/v1/sales/1')
    
    def test_delete_product_successfully(self):
        self.client.post('/api/v1/sales',
                        content_type='application/json',
                        data=json.dumps(self.sale)
                        )
        result = self.client.delete('/api/v1/sales/1')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.data.decode()), {'200': 'Sale deleted successfully'})


