from flask import make_response,jsonify
from app import app

@app.errorhandler(400)
def wrong_param(error):
    return make_response(jsonify({'product not found':' Wrong params for json'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'product not found':' please check id'}), 404)
