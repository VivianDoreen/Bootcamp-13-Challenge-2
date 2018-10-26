import unittest
import json
from app.products import view
from app import app
from cerberus import Validator
from datetime import datetime

date = datetime.now()

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        self.product=json.dumps({
             "product_name": "Nanuscripts books",
             "pdt_description":"Blue",
             "pdt_category":"Books"
            })

        self.null_value_product=json.dumps({
             "product_name": "",
             "pdt_description":"",
             "pdt_category":""
            })
        self.data_to_test = {
                    "date": date.strftime('%A.%B.%Y'),
                    "pdt_category": "Books",
                    "pdt_description": "Blue",
                    "product_code": 1,
                    "product_name": "Nanuscripts books"
                    }
        self.product_with_missing_parameters = json.dumps({
                                            "date":"Fri, 28 Sep 2018 00:00:00 GMT",
                                            "product_code":2,
                                            "product_name":"Chairs" ,
                                            "pdt_description": "Blue"
                                            })
        self.update_product=json.dumps({
                        "product_name":"T-Shirts" ,
                        "pdt_description": "Blue",
                        "pdt_category": "Clothes"
                    })

        