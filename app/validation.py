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
        