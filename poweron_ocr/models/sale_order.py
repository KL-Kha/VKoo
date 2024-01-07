from odoo import models, fields, _
from odoo.exceptions import ValidationError

OCR_SALE_MAPPING = {
    'invoice_date': 'date_order',
    'due_date': 'invoice_date_due',
    'invoice_id': 'client_order_ref',
    'bill_notes': 'note',
    'sale_person': 'user_id',
    'pre_text': 'pretext_id',
}

OCR_SALE_LINE_MAPPING = {
    'line_item/description': 'name',
    'line_item/quantity': 'product_uom_qty',
    'line_item/unit_price': 'price_unit',
    'line_item/tax': 'tax_id',
}

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'ocr.mixin']

    default_ocr_product_id = fields.Many2one(related="company_id.ocr_sale_product_id")
    default_ocr_partner_id = fields.Many2one(related="company_id.ocr_sale_customer_id")
    activate_dokuscan = fields.Boolean(related='company_id.dokuscan_sale_order')

    def ocr_send(self):
        if not self.default_ocr_product_id:
            raise ValidationError(_("Please configure OCR Product for Sale in General Settings"))
        if not self.default_ocr_partner_id:
            raise ValidationError(_("Please configure OCR Default Customer in General Setting"))
        return super().ocr_send()

    def _get_ocr_object_mapping(self):
        return OCR_SALE_MAPPING

    def _get_ocr_object_line_mapping(self):
        return OCR_SALE_LINE_MAPPING

    def _get_object_line_key(self):
        return 'order_line'
    
    def _get_ocr_partner_mapping(self):
        return {
            'receiver_name': 'name',
            'receiver_phone': 'phone',
            'receiver_email': 'email',
            'receiver_website': 'website',
            'receiver_address': 'street',
            'receiver_tax_id': 'vat',
            'receiver_iban': 'iban',
            'so_customer_ref': 'ref',
        }
