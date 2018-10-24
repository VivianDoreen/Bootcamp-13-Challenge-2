"""Product logic for carrying out CRUD (Create, Read, Update, Delete) operations"""
from datetime import datetime

class Product:
    """product class containing CRUD operations of the product"""
    product_code = 1
    products_list = []
    invalid_id = 'Product not found, please check id'

    @staticmethod
    def add_product(pdt_name, pdt_description, pdt_category):
        """Create a new product record."""
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
                return "Product already exists"
            else:
                product["product_code"] += 1
        Product.products_list.append(new_product)
        return new_product

    @staticmethod
    def find_product_by_id(product_id):
        """Get a specific product using the product’s code"""
        result_list = [product for product in Product.products_list if product['product_code'] == product_id]
        if result_list == []:
            return Product.invalid_id
        return result_list

    @staticmethod
    def modify_product(product_id, pdt_name, pdt_description, pdt_category):
        """Modify a specific product using the product’s code"""
        for product in Product.products_list:
            if product_id == product["product_code"]:
                product["product_name"] = pdt_name
                product["pdt_description"] = pdt_description
                product["pdt_category"] = pdt_category
                return product
            return Product.invalid_id
    @staticmethod
    def delete_product(product_id):
        """Delete a specific product using the product’s code"""
        for product in Product.products_list:
            if product_id == product['product_code']:
                Product.products_list.remove(product)
                return "Product deleted"
            
            return Product.invalid_id

    @staticmethod
    def list_all_products():
        """Get all available products"""
        if Product.products_list != []:
            return Product.products_list
        return 'No products available'
