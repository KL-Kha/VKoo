from odoo import fields, models,_

class ResCompany(models.Model):
    _inherit = 'res.company'

    x_anfrage_modus_mode = fields.Boolean(string='Anfrage Modus / RFQ Mode', default=True)