from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    dokuscan_vendor_bill = fields.Boolean(default=True)
    dokuscan_purchase_order = fields.Boolean(default=True)
    dokuscan_sale_order = fields.Boolean(default=True)
    is_dokuscan_overall_tax = fields.Boolean()
    ocr_sale_product_id = fields.Many2one(comodel_name='product.product')
    ocr_sale_customer_id = fields.Many2one(comodel_name='res.partner')
    ocr_purchase_product_id = fields.Many2one(comodel_name='product.product')
    ocr_purchase_vendor_id = fields.Many2one(comodel_name='res.partner')
