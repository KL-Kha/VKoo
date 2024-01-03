from odoo import api, fields, models, _
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
from odoo.exceptions import ValidationError
from urllib.parse import urlparse, parse_qs


_logger = logging.getLogger(__name__)

class GoogleSheetsIntegration(models.Model):
    _name = 'google.sheets.integration'

    # Constants for sheet ranges
    REF_ID_SHEET = 'C5:C'
    CUSTOMER_ID_SHEET = 'D5:D'
    PRODUCT_SHEET_RANGES = [
        {'product_uom_qty': 'E5:E', 'default_code': 'H5:H', 'name': 'I5:I'},
        {'product_uom_qty': 'J5:J', 'default_code': 'K5:K', 'name': 'L5:L'},
        {'product_uom_qty': 'M5:M', 'default_code': 'N5:N', 'name': 'O5:O'},
        {'product_uom_qty': 'P5:P', 'default_code': 'Q5:Q', 'name': 'R5:R'},
        {'product_uom_qty': 'S5:S', 'default_code': 'T5:T', 'name': 'U5:U'},
        {'product_uom_qty': 'V5:V', 'default_code': 'W5:W', 'name': 'X5:X'},
        {'product_uom_qty': 'Y5:Y', 'default_code': 'Z5:Z', 'name': 'AA5:AA'},
        {'product_uom_qty': 'AB5:AB', 'default_code': 'AC5:AC', 'name': 'AD5:AD'},
        {'product_uom_qty': 'AE5:AE', 'default_code': 'AF5:AF', 'name': 'AG5:AG'},
    ]

    def get_spreadsheet_id(self, spreadsheet_url):
        parsed_url = urlparse(spreadsheet_url)
        if 'spreadsheets/d/' in parsed_url.path:
            parts = parsed_url.path.split('/')
            return parts[parts.index('d') + 1]
        elif 'key=' in parsed_url.query:
            return parse_qs(parsed_url.query)['key'][0]
        else:
            raise ValidationError(_("Invalid Google Sheets URL"))
        
    def find_or_create_product(self, product_data):
        # Search for existing product with the given reference or name
        existing_product = self.env['product.product'].search([
            '|', ('default_code', '=', product_data.get('default_code', '')), ('name', '=', product_data.get('name', ''))
        ], limit=1)

        if not existing_product:
            product_vals = {
                'default_code': product_data.get('default_code', ''),
                'name': product_data.get('name', ''),
                # Add other relevant fields as needed
            }
            new_product = self.env['product.product'].create(product_vals)
            return new_product.id
        else:
            return existing_product.id
        
    def create_sale_order(self, ref_id_sheet, customer_id_sheet, products_sheet):
        existing_customer = self.env['res.partner'].search([('ref', '=', ref_id_sheet)])

        if not existing_customer:
            customer_vals = {
                'ref': ref_id_sheet,
                'name': customer_id_sheet,
                'company_id': self.env.user.company_id.id,
            }
            new_customer = self.env['res.partner'].create(customer_vals)

            sale_order_vals = {
                'partner_id': new_customer.id,
            }
            new_sale_order = self.env['sale.order'].create(sale_order_vals)
        else:
            sale_order_vals = {
                'partner_id': existing_customer.id,
            }
            new_sale_order = self.env['sale.order'].create(sale_order_vals)

        # Create sale order lines based on products_sheet
        for product_data in products_sheet:
            product_id = self.find_or_create_product(product_data)
            if product_id:
                product_vals = {
                    'order_id': new_sale_order.id,
                    'product_id': product_id,
                    'product_uom_qty': product_data.get('product_uom_qty', 0),
                    'price_unit': product_data.get('price_unit', 0),
                    # Add other relevant fields as needed
                }
                self.env['sale.order.line'].create(product_vals)

    def fetch_product_data(self, worksheet, row_index):
        # Fetch and organize product data for the specified row_index
        products = []
        for range_info in self.PRODUCT_SHEET_RANGES:
            product_data = {}
            for key, sheet_range in range_info.items():
                values = worksheet.get(sheet_range)
                if values and 0 <= row_index < len(values):
                    product_data[key] = values[row_index][0] if values[row_index] else 0
                else:
                    product_data[key] = 0

                if key == 'default_code':
                    product_data[key] = values[row_index][0] if values and 0 <= row_index < len(values) and values[row_index] else ''
                elif key == 'name':
                    product_data[key] = values[row_index][0] if values and 0 <= row_index < len(values) and values[row_index] else ''

            # Ensure product_uom_qty is not None, set to 0 if it is
            product_data['product_uom_qty'] = product_data.get('product_uom_qty', 0)

            products.append(product_data)

        return products

    @api.model
    def get_google_sheet_data(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials_path = '/opt/odoo/customize/gsheet2odoo/data/credentials.json'

        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        gc = gspread.authorize(credentials)

        spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1UiHYxmQqCWkuKxbIZusjuZ-b8TFAO6b_jMy-U2j--v4/edit#gid=1335899468'
        spreadsheet_id = self.get_spreadsheet_id(spreadsheet_url)

        worksheet = gc.open_by_key(spreadsheet_id).sheet1

        ref_ids = worksheet.get(self.REF_ID_SHEET)
        customer_ids = worksheet.get(self.CUSTOMER_ID_SHEET)

        for index, (ref_id, customer_id) in enumerate(zip(ref_ids, customer_ids)):
            ref_id = ref_id[0] if ref_id else False
            customer_id = customer_id[0] if customer_id else False

            if ref_id and customer_id:
                products = self.fetch_product_data(worksheet, index)
                self.create_sale_order(ref_id, customer_id, products)

        return True