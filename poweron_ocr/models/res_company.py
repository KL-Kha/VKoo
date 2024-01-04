from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    is_dokuscan_overall_tax = fields.Boolean()
    ocr_purchase_product_id = fields.Many2one(comodel_name='product.product')
    ocr_purchase_vendor_id = fields.Many2one(comodel_name='res.partner')
