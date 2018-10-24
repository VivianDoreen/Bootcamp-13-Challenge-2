"""Product Endpoints to be used when carrying out crud operations"""
from flask import jsonify, request, abort, make_response
from app import app
from app.products.model import Product
from app import handle_errors
import jwt
import datetime
from cerberus import Validator

@app.route('/')
def index():
    """This is the welcome page"""
    return jsonify({"Hello Admin":"Welcome to ManagerStore"})

@app.route('/api/v1/products', methods=['GET'])
def get_products():
    """This method gets all available products"""
    return jsonify({200: Product.list_all_products()}), 200

@app.route('/api/v1/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """This method gets a specific product using the product’s id"""
    if isinstance(Product.find_product_by_id(product_id), dict):
        return jsonify(Product.find_product_by_id(product_id)), 200
    return jsonify({404: Product.find_product_by_id(product_id)}), 404

@app.route('/api/v1/products', methods=['POST'])
def create_product():
    """This methods creates a new product record"""
    if not request.json or not 'product_name' in request.json or not 'pdt_category' in request.json or not 'pdt_description' in request.json:
        abort(400)
    new_product = request.get_json() or {}

    schema = {
            'product_name': {'required': True, 'type': 'string','empty': False, 'regex': '[a-zA-Z]{2,20}'},
            'pdt_description': {'required': True, 'type': 'string','empty': False, 'minlength':2, 'regex': '[a-zA-Z]+'},
            'pdt_category': {'required': True, 'type': 'string', 'empty': False, 'minlength':2, 'regex': '[a-zA-Z]+'},
        }
    v = Validator(schema)
    if not v(new_product):
            return "Check your input values.\n -Product_name*: Required, must be a string and minlength : 2 characters\n -pdt_description* : Required, must be a string and minlength : 5 characters\n -Pdt_category* : Required , must be a string and minlength : 2 characters", 400
    

    new_product_return = Product.add_product(new_product['product_name'],
                                             new_product['pdt_description'],
                                             new_product['pdt_category'])

    if new_product_return == "Product already exists":
        return jsonify({403 : new_product_return}), 403
    return jsonify({201: 'Product successfully added'}), 201

@app.route('/api/v1/products/<int:product_id>', methods=['PUT'])
def change_product(product_id):
    """
    This endpoint modifies a product
    :param version: 
    :param product_id: 
    :return: 
    """
    new_product = request.get_json() or {}
    if Product.modify_product(product_id, new_product['product_name'],
                              new_product['pdt_description'],
                              new_product['pdt_category']) == 'Product not found, please check id':
        return jsonify({404: 'Product not found, please check id'}), 404
    Product.modify_product(product_id, new_product['product_name'],
                           new_product['pdt_description'], new_product['pdt_category'])
    return jsonify({201: 'Product has been modified successfully'}), 201

@app.route('/api/v1/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """"This method deletes a product using the product's id"""
    if isinstance(Product.find_product_by_id(product_id), dict):
        return jsonify({200:Product.delete_product(product_id)}), 200
    return jsonify({404: Product.find_product_by_id(product_id)}), 404
