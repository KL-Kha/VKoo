from odoo import models, fields, api
from odoo.tools.misc import formatLang


class AccountMove(models.Model):
    _inherit = 'account.move'

    print_logo = fields.Boolean(string='Logo', default=True)
    logo_position = fields.Selection([('left', 'Left'),
                                      ('center', 'Center'),
                                      ('right', 'Right')], string='Logo Position', default='left')
    pretext = fields.Html(string='Pre Text')
    terms_and_conditions = fields.Html(string='Terms and Conditions')
    pretext_id = fields.Many2one('invoice.template.pretext', string='Pre-Text')
    terms_and_conditions_id = fields.Many2one('invoice.template.terms.and.conditions',
                                              string='Terms and Conditions')
    is_added_prefix = fields.Boolean(default=False)

    @api.onchange('pretext_id')
    def _onchange_pretext_id(self):
        self.pretext = self.pretext_id.pretext

    @api.onchange('terms_and_conditions_id')
    def _onchange_terms_and_conditions_id(self):
        self.terms_and_conditions = self.terms_and_conditions_id.terms_and_conditions

    @api.model
    def _get_tax_totals(self, partner, tax_lines_data, amount_total, amount_untaxed, currency):
        res = super()._get_tax_totals(partner, tax_lines_data, amount_total, amount_untaxed, currency)
        subtotal_amount = sum(self.invoice_line_ids.filtered(lambda x: not x._is_downpayment_line()).mapped('price_subtotal'))
        total_amount = subtotal_amount + self.amount_tax
        res.update({
            'formatted_subtotal_amount': formatLang(self.env, subtotal_amount, currency_obj=self.currency_id),
            'formatted_total_amount': formatLang(self.env, total_amount, currency_obj=self.currency_id),
        })
        return res

    def _get_not_downpayment_lines(self):
        invoice_lines = self.invoice_line_ids.sorted(key=lambda l: (-l.sequence, l.date, l.move_name, -l.id), reverse=True)
        downpayment_sequence = 0
        for line in self.invoice_line_ids:
            if line.display_type == 'line_section':
                if self.invoice_line_ids[line.sequence-1] and not self.invoice_line_ids[line.sequence-1]._is_downpayment_line():
                    downpayment_sequence = line.sequence
        if downpayment_sequence:
            invoice_lines = self.invoice_line_ids.filtered(lambda x: (not x._is_downpayment_line() and x.sequence < downpayment_sequence) or x.display_type == 'line_note')
        return invoice_lines

    def _check_confirm_milestone_payment(self):
        for line in self.invoice_line_ids:
            if line._is_downpayment_line():
                if line.sale_line_ids and line.sale_line_ids[0].invoice_lines and line.sale_line_ids[0].invoice_lines[0].parent_state == 'posted':
                    return True
        return False

    def _is_milestone_invoice(self):
        if len(self.invoice_line_ids) == 1 and self.invoice_line_ids[0]._is_downpayment_line():
            return True
        return False
    
    def _get_invoice_filename(self):
        invoice_number = self.name.replace('/','_')
        customer_lastname = (', ' +  self.partner_id.lastname) if self.partner_id.lastname else ''
        order_description = (', ' +  self.invoice_line_ids[0].sale_line_ids.order_id.custom_description) if self.invoice_line_ids and self.invoice_line_ids[0].sale_line_ids.order_id.custom_description else ''

        if self.state == 'cancel':
            filename = f"Storno-{invoice_number}{customer_lastname}{order_description}"
        else:
            filename = f"{invoice_number}{customer_lastname}{order_description}"
        return filename

    def _get_invoice_report_filename(self):
        return self._get_invoice_filename()


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _is_downpayment_line(self):
        self.ensure_one()
        downpayment_product = self.env['ir.config_parameter'].sudo().get_param('sale.default_deposit_product_id')
        if self.product_id and self.product_id.id == int(downpayment_product):
            return True
        return False