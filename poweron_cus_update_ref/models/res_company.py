from odoo import fields, models,_

class ResCompany(models.Model):
    _inherit = 'res.company'

    use_update_customer_by_excel = fields.Boolean('Excel', default=False)
    excel_path = fields.Char(string='Excel Patch')