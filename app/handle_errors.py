from flask import make_response,jsonify
from app import app

@app.errorhandler(400)
def wrong_param(error):
    return make_response(jsonify({'product not found':'Wrong params for json'}), 400)

@app.errorhandler(405)
def wrong_url(error):
    return make_response(jsonify({'Method not allowed':'Try Again'}), 405)

@app.errorhandler(409)
def already_exists(error):
    return make_response(jsonify({'Message' : 'Product already exists'}), 409)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'product not found':'please check id'}), 404)

@app.errorhandler(422)
def wrong_input(error):
    return make_response("Check your input values."
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
            ), 422