from odoo import models, fields

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def _get_invoice_filename(self):
        invoice_number = self.sequence_number or 'NoInvoiceNumber'
        invoice_number = self.name.replace('INV/', '')
        customer_lastname = self.partner_id.parent_name or 'NoCustomerLastName'
        order_description = self.invoice_line_ids[0].name if self.invoice_line_ids and self.invoice_line_ids[0].name else 'NoOrderDescription'

        if self.state == 'cancel':
            filename = f"Storno-RE_{invoice_number}, {customer_lastname}, {order_description}"  
        else:
            down_payment_lines = self.invoice_line_ids.filtered(lambda line: 'Down payment' in line.name)
            if down_payment_lines:
                filename = f"ARE_{invoice_number}, {customer_lastname}, {order_description}"
            else:
                filename = f"RE_{invoice_number}, {customer_lastname}, {order_description}"
        return filename

    def _get_invoice_report_filename(self):
        return self._get_invoice_filename()