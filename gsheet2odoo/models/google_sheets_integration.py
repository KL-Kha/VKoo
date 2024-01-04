from odoo import api, fields, models, _
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
from odoo.exceptions import ValidationError
from urllib.parse import urlparse, parse_qs
import pandas as pd
import re

_logger = logging.getLogger(__name__)


class GoogleSheetsIntegration(models.Model):
    _name = 'google.sheets.integration'

    spreadsheet_url = fields.Char('Spreadsheet Url')
    credentials_path = fields.Char('Credentials Path')

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
        if product_data['default_code'] and product_data['name']:
            # Search for existing product with the given reference or name
            existing_product = self.env['product.product'].search([
                '|', ('default_code', '=', product_data['default_code']), ('name', '=', product_data['name'])
            ], limit=1)

            if not existing_product:
                product_vals = {
                    'default_code': product_data['default_code'],
                    'name': product_data['name'],
                }
                new_product = self.env['product.product'].create(product_vals)
                return new_product
            else:
                return existing_product
        else:
            return False

    def create_sale_order(self, ref_id_sheet, customer_id_sheet):
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

        self.env.cr.commit()
        return new_sale_order

    @api.model
    def get_google_sheet_data(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        # credentials_path = '/opt/odoo/customize/gsheet2odoo/data/test_credentials.json'
        credentials_path = self.env.user.company_id.credentials_path

        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        gc = gspread.authorize(credentials)

        # spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1UiHYxmQqCWkuKxbIZusjuZ-b8TFAO6b_jMy-U2j--v4/edit#gid=1335899468'
        spreadsheet_url = self.env.user.company_id.spreadsheet_url
        spreadsheet_id = self.get_spreadsheet_id(spreadsheet_url)
        worksheet = gc.open_by_key(spreadsheet_id).sheet1

        worksheet_value = worksheet.get_all_values()
        worksheet_value_correct = worksheet_value[4:]

        data_group_month = pd.DataFrame(worksheet_value_correct).groupby([1, 2])

        for key, vals in data_group_month.groups.items():
            group_by_data_user = data_group_month.get_group(key)
            sale_order_id = self.create_sale_order(key[1], group_by_data_user[3][vals[0]])
            for i in group_by_data_user.index:
                PRODUCT_SHEET_RANGES = [
                    {'product_uom_qty': group_by_data_user[4][i], 'default_code': group_by_data_user[7][i],
                     'name': group_by_data_user[8][i]},
                    {'product_uom_qty': group_by_data_user[9][i], 'default_code': group_by_data_user[10][i],
                     'name': group_by_data_user[11][i]},
                    {'product_uom_qty': group_by_data_user[12][i], 'default_code': group_by_data_user[13][i],
                     'name': group_by_data_user[14][i]},
                    {'product_uom_qty': group_by_data_user[15][i], 'default_code': group_by_data_user[16][i],
                     'name': group_by_data_user[17][i]},
                    {'product_uom_qty': group_by_data_user[18][i], 'default_code': group_by_data_user[19][i],
                     'name': group_by_data_user[20][i]},
                    {'product_uom_qty': group_by_data_user[21][i], 'default_code': group_by_data_user[22][i],
                     'name': group_by_data_user[23][i]},
                    {'product_uom_qty': group_by_data_user[24][i], 'default_code': group_by_data_user[25][i],
                     'name': group_by_data_user[26][i]},
                    {'product_uom_qty': group_by_data_user[27][i], 'default_code': group_by_data_user[28][i],
                     'name': group_by_data_user[29][i]},
                    {'product_uom_qty': group_by_data_user[30][i], 'default_code': group_by_data_user[31][i],
                     'name': group_by_data_user[32][i]},
                ]
                for product_data in PRODUCT_SHEET_RANGES:
                    product_id = self.find_or_create_product(product_data)
                    if product_id:
                        product_vals = {
                            'order_id': sale_order_id.id,
                            'product_id': product_id.id,
                            'product_uom_qty': product_data['product_uom_qty'] if product_data[
                                'product_uom_qty'] else 0,
                            # Add other relevant fields as needed
                        }
                        self.env['sale.order.line'].create(product_vals)
