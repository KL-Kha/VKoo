from odoo import models, fields, _
from odoo.exceptions import ValidationError

OCR_SALE_MAPPING = {
    'invoice_date': 'date_order',
    'due_date': 'invoice_date_due',
    'invoice_id': 'reference',
    'bill_notes': 'note',
}

OCR_SALE_LINE_MAPPING = {
    'line_item/description': 'name',
    'line_item/quantity': 'product_uom_qty',
    'line_item/unit_price': 'price_unit',
    'line_item/tax': 'tax_id',
}

CUSTOMER_SEARCH_FIELDS = ['vat', 'name', 'email']


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'ocr.mixin']

    default_ocr_product_id = fields.Many2one(related="company_id.ocr_purchase_product_id")
    default_ocr_partner_id = fields.Many2one(related="company_id.ocr_purchase_vendor_id")

    def ocr_send(self):
        if not self.default_ocr_product_id:
            raise ValidationError(_("Please configure OCR Product for Sale in General Settings"))
        if not self.default_ocr_partner_id:
            raise ValidationError(_("Please configure OCR Default Customer in General Setting"))
        return super().ocr_send()

    def _get_vendor_search_fields(self):
        return CUSTOMER_SEARCH_FIELDS

    def _get_ocr_object_mapping(self):
        return OCR_SALE_MAPPING

    def _get_ocr_object_line_mapping(self):
        return OCR_SALE_LINE_MAPPING

    def _get_object_line_key(self):
        return 'order_line'
