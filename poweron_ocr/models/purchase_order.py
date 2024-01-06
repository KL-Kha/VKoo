from odoo import models, fields, _
from odoo.exceptions import ValidationError

OCR_PURCHASE_MAPPING = {
    # 'invoice_date': 'invoice_date',
    # 'due_date': 'invoice_date_due',
    # 'bill_notes': 'narration',
}

OCR_PURCHASE_LINE_MAPPING = {
    'line_item/description': 'name',
    'line_item/quantity': 'product_qty',
    'line_item/unit_price': 'price_unit',
    'line_item/tax': 'taxes_id',
}


class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = ['purchase.order', 'ocr.mixin']

    default_ocr_product_id = fields.Many2one(related="company_id.ocr_purchase_product_id")
    default_ocr_partner_id = fields.Many2one(related="company_id.ocr_purchase_vendor_id")
    activate_dokuscan = fields.Boolean(related='company_id.dokuscan_purchase_order')

    def ocr_send(self):
        if not self.default_ocr_product_id:
            raise ValidationError(_("Please setup Default Product for Purchase in Dokuscan Settings"))
        if not self.default_ocr_partner_id:
            raise ValidationError(_("Please setup Default Vendor in Dokuscan Setting"))
        return super().ocr_send()

    def _get_ocr_object_line_mapping(self):
        return OCR_PURCHASE_LINE_MAPPING

    def _get_object_line_key(self):
        return 'order_line'
