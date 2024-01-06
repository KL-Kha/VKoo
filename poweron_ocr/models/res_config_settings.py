from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    dokuscan_vendor_bill = fields.Boolean(related='company_id.dokuscan_vendor_bill', readonly=False, string="Dokuscan Vendor Bill")
    dokuscan_purchase_order = fields.Boolean(related='company_id.dokuscan_purchase_order', readonly=False, string="Dokuscan Purchase Order")
    dokuscan_sale_order = fields.Boolean(related='company_id.dokuscan_sale_order', readonly=False, string="Dokuscan Sales Order")
    is_dokuscan_overall_tax = fields.Boolean(related='company_id.is_dokuscan_overall_tax', readonly=False, string="DokuScan Overall Tax")

    ocr_sale_product_id = fields.Many2one(related='company_id.ocr_sale_product_id', readonly=False, string="Default OCR Product for Sale Order")
    ocr_sale_customer_id = fields.Many2one(related='company_id.ocr_sale_customer_id', readonly=False, string="Default OCR Customer for Sale Order")

    ocr_purchase_product_id = fields.Many2one(related='company_id.ocr_purchase_product_id', readonly=False, string="Default OCR Product for Purchase")
    ocr_purchase_vendor_id = fields.Many2one(related='company_id.ocr_purchase_vendor_id', readonly=False, string="Default OCR Partner for Purchase")
