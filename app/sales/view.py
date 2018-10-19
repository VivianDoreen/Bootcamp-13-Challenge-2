"""Sales Endpoints to be used when carrying out crud operations"""
from flask import jsonify, request, abort, make_response
from app import app
from app.sales.model import Sale
from app import handle_errors

@app.route('/api/v1/sales', methods=['GET'])
def get_sales():
    """This method gets all available sales"""
    return jsonify({200: Sale.list_all_sales()}), 200

@app.route('/api/v1/sales/<int:sales_id>', methods=['GET'])
def get_sale(sales_id):
    """This method gets a specific sale using the sale’s id"""
    if isinstance(Sale.find_sale_by_id(sales_id), dict):
        return jsonify(Sale.find_sale_by_id(sales_id)), 200
    # if Sale.find_sale_by_id(sales_id) == []:
    #     return "Id doesnot exist"
    return jsonify({404: Sale.find_sale_by_id(sales_id)}), 404

@app.route('/api/v1/sales', methods=['POST'])
def create_sale():
    """This methods creates a new product record"""
    if not request.json or not 'product_code' in request.json or not 'product_name' in request.json or not 'unit_measure' in request.json or not 'quantity' in request.json or not 'unit_price' in request.json or not 'total_price' in request.json:
        abort(400)
    new_sale = request.get_json() or {}
    new_sale_return = Sale.add_sale(new_sale['product_code'],
                                    new_sale['product_name'],
                                    new_sale['unit_measure'],
                                    new_sale['quantity'],
                                    new_sale['unit_price'],
                                    new_sale['total_price']
                                    )
    if new_sale_return == "Sale already exists":
        return jsonify({403 : new_sale_return}), 403
    return jsonify({201: 'Sale successfully added'}), 201

@app.route('/api/v1/sales/<int:sales_id>', methods=['PUT'])
def change_sale(sales_id):
    """
    This endpoint modifies a product
    :param version: 
    :param product_id: 
    :return: 
    """
    new_product = request.get_json() or {}
    if Sale.modify_sale(sales_id,
                        new_product['product_code'],
                        new_product['product_name'],
                        new_product['unit_measure'],
                        new_product['quantity'],
                        new_product['unit_price'],
                        new_product['total_price']) == 'Sale not found, please check id':
        return jsonify({404: 'Sale not found, please check id'}), 404
    Sale.modify_sale(sales_id,
                     new_product['product_code'],
                     new_product['product_name'],
                     new_product['unit_measure'],
                     new_product['quantity'],
                     new_product['unit_price'],
                     new_product['total_price'])
    return jsonify({201: 'Sale has been modified successfully'}), 201

@app.route('/api/v1/sales/<int:sale_id>', methods=['DELETE'])
def delete_sale(sale_id):
    """"This method deletes a sale using the sale id"""
    if isinstance(Sale.find_sale_by_id(sale_id), dict):
        return jsonify({200:Sale.delete_sale(sale_id)}), 200
    return jsonify({404: Sale.find_sale_by_id(sale_id)}), 404
