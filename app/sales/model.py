"""Sales logic for carrying out CRUD (Create, Read, Update, Delete) operations"""
from datetime import datetime

class Sale:
    """product class containing CRUD operations of the product"""
    sales_id = 1
    sales_record = []
    invalid_id = 'Sale not found, please check id'

    @staticmethod
    def add_sale(product_code, pdt_name, unit_measure, quantity, unit_price, total_price):
        """Create a new sale record."""
        sale = {}
        date = datetime.now()
        product_code = product_code
        product_name = pdt_name
        unit_measure = unit_measure
        quantity = quantity
        unit_price = unit_price
        total_price = total_price

        new_sale = {
            "date": date.strftime('%A.%B.%Y'),
            "sales_id":Sale.sales_id,
            "product_code": product_code,
            "product_name" : product_name,
            "unit_measure" : unit_measure,
            "quantity" : quantity,
            "unit_price" : unit_price,
            "total_price" : total_price
            }

        for sale in Sale.sales_record:
            if Sale.sales_record == []:
                Sale.sales_record.append(new_sale)
                return sale
            if (new_sale['product_code'],
                new_sale['product_name'],
                new_sale['unit_measure'],
                new_sale['quantity'],
                new_sale['unit_price'],
                new_sale['total_price']) == (sale['product_code'],
                                            sale['product_name'],
                                            sale['unit_measure'],
                                            sale['quantity'],
                                            sale['unit_price'],
                                            sale['total_price']
                                            ):
                return "Sale already exists"
            else:
                sale["sales_id"] += 1
        Sale.sales_record.append(new_sale)
        return new_sale

    @staticmethod
    def find_sale_by_id(sale_id):
        """Get a specific product using the product’s code"""
        result_sale = [sale for sale in Sale.sales_record if sale["sales_id"] == sale_id]
        if result_sale == []:                
            return Sale.invalid_id
        return result_sale
    @staticmethod
    def modify_sale(sales_id, product_code, pdt_name, unit_measure, quantity, unit_price, total_price):
        """Modify a specific sale using the sale id"""
        result_sale = [sale for sale in Sale.sales_record if sale["sales_id"] == sales_id]
        if result_sale == []:                
            return Sale.invalid_id
        result_sale[0]["product_code"] = product_code
        result_sale[0]["pdt_name"] = pdt_name
        result_sale[0]["unit_measure"] = unit_measure
        result_sale[0]["quantity"] = quantity
        result_sale[0]["unit_price"] = unit_price
        result_sale[0]["total_price"] = total_price
        return result_sale
    @staticmethod
    def delete_sale(sale_id):
        """Delete a specific sale using the sale id"""
        result_sale = [sale for sale in Sale.sales_record if sale["sales_id"] == sale_id]
        if result_sale == []:                
            return Sale.invalid_id
        return "Sale deleted successfully" 

    @staticmethod
    def list_all_sales():
        """Get all available products"""
        if Sale.sales_record != []:
            return Sale.sales_record
        return 'No Sales available'
