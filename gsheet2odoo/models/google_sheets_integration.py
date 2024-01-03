from odoo import models, api
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging

_logger = logging.getLogger(__name__)

class GoogleSheetsIntegration(models.Model):
    _name = 'google.sheets.integration'

    @api.model
    def get_google_sheet_data(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('/path/to/your/credentials.json', scope)
        gc = gspread.authorize(credentials)

        # Open the spreadsheet
        worksheet = gc.open("Your Spreadsheet Title").sheet1

        # Get all values
        return worksheet.get_all_values()

    def match_or_create_customer(self, customer_id, customer_name):
        """
        Match a customer my name. If no match found, create a new one.
        """
        Customer = self.env['res.partner']
        # Approximate match by name
        customer = Customer.search([('name', 'ilike', customer_name)], limit=1)
        if customer:
            return customer
        else:
            # Create new customer
            return Customer.create({'name': customer_name, 'customer_id': customer_id})

    def match_product(self, product_id):
        """
        Search for a product by its 'defaultcode'
        If found, return the product. Else none.
        """
        Product = self.env['product.product']
        product = Product.search([('id', '=', product_id)], limit=1)
        return product if product else None

    @api.model
    def import_to_sale_order(self):
        """
        A known problem with this function should be fixed.
        Problem:
        The function imports all rows in the G-Sheet into the same SaleOrder.
        Expected Behavior:
        The business requirement is to create multiple SaleOrders, based on unique customers found in Column-D of G-Sheet.
        Assume that each unique customer only has 1 SaleOrder.
        """
        values = self.get_google_sheet_data()
        for index, row in enumerate(values):
            try:
                # Do the column mapping between sale.order fields and G-Sheet here.
                customer_id = row[1]
                customer_name = row[2]
                product_id = row[3]

                customer = self.match_or_create_customer(customer_id, customer_name)
                product = self.match_product(product_id)

                if product:
                    order_line = {
                        'product_id': product.id,
                        'name': product.name,
                        'product_uom_qty': 1,  # Default quantity
                        'price_unit': product.lst_price,
                    }

                    self.env['sale.order'].create({
                        'partner_id': customer.id,
                        'order_line': [(0, 0, order_line)],
                    })
                else:
                    _logger.error(f"Product with ID {product_id} not found for row {index + 1}")
            except Exception as e:
                _logger.error(f"Failed to import row {index + 1}: {e}")
