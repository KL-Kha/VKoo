import logging

from odoo import models, fields, _

_logger = logging.getLogger(__name__)

OCR_INVOICE_MAPPING = {
    'invoice_date': 'invoice_date',
    'due_date': 'invoice_date_due',
    'invoice_id': 'ref',
    'bill_notes': 'narration',
}

OCR_VENDOR_MAPPING = {
    'supplier_name': 'name',
    'supplier_phone': 'phone',
    'supplier_email': 'email',
    'supplier_website': 'website',
    'supplier_address': 'street',
    'supplier_tax_id': 'vat',
    'supplier_iban': 'iban',
}

OCR_INVOICE_LINE_MAPPING = {
    'line_item/description': 'name',
    'line_item/quantity': 'quantity',
    'line_item/unit_price': 'price_unit',
    'line_item/tax': 'tax_ids',
}


class VendorBill(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'ocr.mixin']

    activate_dokuscan = fields.Boolean(related='company_id.dokuscan_vendor_bill')

    def _get_ocr_object_mapping(self):
        return OCR_INVOICE_MAPPING

    def _get_ocr_object_line_mapping(self):
        return OCR_INVOICE_LINE_MAPPING

    def _get_object_line_key(self):
        return 'invoice_line_ids'
