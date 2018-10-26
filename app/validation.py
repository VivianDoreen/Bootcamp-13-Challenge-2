from cerberus import Validator

class ValidateInput:
    @staticmethod
    def validate_input():
        schema = {
                    'product_name': {
                                    'required': True,
                                    'type': 'string',
                                    'empty': False,
                                    'regex': r'^[a-zA-Z]{2,18}(?:[\s_-]{1}[a-zA-Z]+)*$'
                                    },
                    'pdt_description': {
                                    'required': True,
                                    'type': 'string',
                                    'empty': False,
                                    'minlength':2,
                                    'regex': r'^[a-zA-Z].*[\s.]*$'},
                    'pdt_category': {
                                    'required': True,
                                    'type': 'string',
                                    'empty': False,
                                    'minlength':2,
                                    'regex': r'^[a-zA-Z].*[\s.]*$'}
                }
        return Validator(schema)

    @staticmethod
    def validate_input_sales():
        schema_sales = {
                    'product_code':{
                                    'required': True,
                                    'type': 'integer',
                                    'empty': False,
                                    'regex': r'^[1-9]{2,18}*$'
                                    },

                    'product_name': {
                                    'required': True,
                                    'type': 'string',
                                    'empty': False,
                                    'regex': r'^[a-zA-Z]{2,18}(?:[\s_-]{1}[a-zA-Z]+)*$'
                                    },

                    'unit_measure': {
                                    'required': True,
                                    'type': 'string',
                                    'empty': False,
                                    'regex': r'^[a-zA-Z].*[\s.]*$'
                    },
                    'quantity': {
                                   'required': True,
                                    'type': 'integer',
                                    'empty': False,
                                    'regex': r'^[1-9]{2,18}*$'
                                    },
                    'unit_price':{
                                   'required': True,
                                    'type': 'integer',
                                    'empty': False,
                                    'regex': r'^[1-9]{2,18}*$'
                                    },
                    'total_price':{
                                   'required': True,
                                    'type': 'integer',
                                    'empty': False,
                                    'regex': r'^[1-9]{2,18}*$'
                                    }
                }
        return Validator(schema_sales)

        