# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import literal_eval

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    use_update_customer_by_excel = fields.Boolean('Excel',related='company_id.use_update_customer_by_excel',readonly=False)
    excel_path = fields.Char('Excel Patch',related='company_id.excel_path', readonly=False)

    def update_customer_by_excel(self):
        record = self.env['excel.update.customer.ref'].search([])
        record.get_update_excel_customer()