# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import literal_eval

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    use_google_sheet_connector = fields.Boolean('Google Sheet Connector - SO',related='company_id.use_google_sheet_connector',readonly=False)
    spreadsheet_url = fields.Char('Spreadsheet Url',related='company_id.spreadsheet_url', readonly=False)
    credentials_path = fields.Char('Credentials Path',related='company_id.credentials_path', readonly=False)

    def generate_ggsheet2odoo(self):
        record = self.env['google.sheets.integration'].search([])
        record.get_google_sheet_data()