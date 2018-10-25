"""Product logic for carrying out CRUD (Create, Read, Update, Delete) operations"""
from flask import abort
from datetime import datetime

class Product:
    """product class containing CRUD operations of the product"""
    product_code = 1
    products_list = []

    @staticmethod
    def add_product(pdt_name, pdt_description, pdt_category):
        """
        Adds product to list
        :return: the product that has just been added
        """
        product = {}
        date = datetime.now()
        name = pdt_name
        description = pdt_description
        category = pdt_category
        new_product = {
            "date": date.strftime('%A.%B.%Y'),
            "product_name": name,
            "pdt_description":description,
            "pdt_category":category,
            "product_code": Product.product_code
        }
        for product in Product.products_list:
            if Product.products_list == []:
                Product.products_list.append(new_product)
                return product
            if (new_product['product_name'],
                    new_product['pdt_description'],
                    new_product['pdt_category']) == (product['product_name'],
                                                     product['pdt_description'],
                                                     product['pdt_category']):
                abort(409)
            else:
                product["product_code"] += 1
        Product.products_list.append(new_product)
        return new_product

    @staticmethod
    def find_product_by_id(product_id):
        """
        This method gets a single product
        :param product_id: 
        :return: single product and status code 200 
        """
        result_list =[
                        product for product in 
                        Product.products_list
                        if product['product_code'] == product_id
                     ]
        if result_list == []:
            abort(404)
        return result_list

    @staticmethod
    def modify_product(product_id, pdt_name, pdt_description, pdt_category):
        """Modify a specific product using the product’s code"""
        product_result =[
                        product for product in 
                        Product.products_list
                        if product['product_code'] ==  product_id
                     ]
        if product_result == []:
            abort(404)
  
        product_result[0]["product_name"] = pdt_name
        product_result[0]["pdt_description"] = pdt_description
        product_result[0]["pdt_category"] = pdt_category
        return product_result
        
    @staticmethod
    def delete_product(product_id):
        """Delete a specific product using the product’s code"""
        for product in Product.products_list:
            if product_id == product['product_code']:
                Product.products_list.remove(product)
                return "Product deleted"
            
            abort(404)

    @staticmethod
    def list_all_products():
        """
        This method gets all entries
        :return: all products in the list
        """
        if Product.products_list != []:
            return Product.products_list
        return 'No products available'
