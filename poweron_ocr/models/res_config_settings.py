from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_dokuscan_overall_tax = fields.Boolean(related='company_id.is_dokuscan_overall_tax', readonly=False, string="DokuScan Overall Tax")
    ocr_purchase_product_id = fields.Many2one(related='company_id.ocr_purchase_product_id', readonly=False, string="Default OCR Product for Purchase")
    ocr_purchase_vendor_id = fields.Many2one(related='company_id.ocr_purchase_vendor_id', readonly=False, string="Default OCR Partner for Purchase")
