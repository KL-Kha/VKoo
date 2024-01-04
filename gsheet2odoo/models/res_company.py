from odoo import fields, models,_

class ResCompany(models.Model):
    _inherit = 'res.company'

    use_google_sheet_connector = fields.Boolean('Google Sheet Connector - SO', default=False)
    spreadsheet_url = fields.Char(string='Spreadsheet Url')
    credentials_path = fields.Char(string='Credentials Path')