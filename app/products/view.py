"""Product Endpoints to be used when carrying out crud operations"""
from flask import jsonify, request, abort, make_response
from app import app
from app.products.model import Product
from app import handle_errors
from app.validation import ValidateInput
import jwt
import datetime

@app.route('/')
def index():
    """
    Index route
    """
    return ("Welcome to ManagerStore")

@app.route('/api/v1/products', methods=['GET'])
def get_products():
    """
    This endpoint gets a all products
    """
    return jsonify({"Product List": Product.list_all_products()}), 200

@app.route('/api/v1/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    This endpoint gets a single product
    :param product_id: 
    """
    if isinstance(Product.find_product_by_id(product_id), list):
        return jsonify(Product.find_product_by_id(product_id))

@app.route('/api/v1/products', methods=['POST'])
def create_product():
    """
    This endpoint adds a product
    """    
    if (not request.json or not 'product_name' in request.json
                         or not 'pdt_category' in request.json
                         or not 'pdt_description' in request.json
                         ):
        abort(400)
    new_product = request.get_json() or {}
    validate = ValidateInput.validate_input()
    if not validate(new_product):
        abort(422)
    new_product_return = Product.add_product(
                                             new_product['product_name'],
                                             new_product['pdt_description'],
                                             new_product['pdt_category']
                                            )
    if new_product_return:
        return jsonify({"message":new_product_return}), 201
    return jsonify({'message': new_product_return})

@app.route('/api/v1/products/<int:product_id>', methods=['PUT'])
def change_product(product_id):
    """
    This endpoint modifies a product
    :param product_id: 
    """
    new_product = request.get_json() or {}
    return jsonify({"Message":Product.modify_product(
                                    product_id,
                                    new_product['product_name'],
                                    new_product['pdt_description'],
                                    new_product['pdt_category']
                                )}), 201

@app.route('/api/v1/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """"This method deletes a product using the product's id"""
    if isinstance(Product.find_product_by_id(product_id), list):
        return jsonify({"Message":Product.delete_product(product_id)})
