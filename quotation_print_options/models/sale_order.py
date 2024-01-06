# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import re
import json
import logging
from datetime import date, datetime

from odoo import models, api, fields, _
from odoo.tools import format_date, formatLang


_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Druckoptionen/Print Options
    print_logo = fields.Boolean(string='Logo', default=True, copy=True)
    print_all_single_prices = fields.Boolean(string='Alle Einzelpreise anzeigen', copy=True)
    pretext_id = fields.Many2one('sale.order.template.pretext', string='Pre-Text')
    pretext = fields.Html(string='Pre Text')
    terms_and_conditions_id = fields.Many2one('sale.order.template.terms.and.conditions', string='Post-text 1')
    terms_and_conditions = fields.Html(string='Terms and Conditions')
    confirmation_letter_id = fields.Many2one('sale.order.confirmation.letter', string='Post-text 2')
    confirmation_letter = fields.Html(string='Confirmation Letter')
    teaser_pic = fields.Image(string="Image", copy=False)
    logo_position = fields.Selection([('left', 'Left'),
                                      ('center', 'Center'),
                                      ('right', 'Right')], string='Logo Position', default="left", copy=True)
    show_product_image = fields.Boolean(string='Show Product Image', copy=True)
    hide_zero_price = fields.Boolean(string="Hide 0 Prices", default=True, copy=True)
    l10n_de_template_data_inherit = fields.Binary(compute='_compute_l10n_de_template_data_inherit')

    page_break_before_invoice_plan = fields.Boolean(string="Seitenumbruch vor Zahlungsplan", default=True, copy=True)
    page_break_after_pre_text = fields.Boolean(string="Seitenumbruch nach Vortext", default=False, copy=True)
    page_break_before_post_text = fields.Boolean(string="Seitenumbruch vor Nachtext 1", default=True, copy=True)
    page_break_before_post_text_2 = fields.Boolean(string="Seitennumbruch vor Nachtext 2", default=True, copy=True)
    show_invoice_plan = fields.Boolean(string="Rechnungsplan anzeigen", default=True, copy=True)
    show_optional_product_price = fields.Boolean('Show Optional Product Price', default=True, copy=True)
    show_section_price = fields.Boolean('Show Section Price', default=True, copy=True)
    show_section_product = fields.Boolean('Show Section Product', default=True, copy=True)
    show_partner_shipping = fields.Boolean('Show Installation Address', default=True, copy=True)
    show_order_confirmation = fields.Boolean('Show Order Confirmation block', default=False)
    discount_total = fields.Monetary('Discount Amount', compute='_compute_discount_total')
    show_teaser_pic = fields.Boolean('Show teaser picture')
    show_optional_product = fields.Boolean('Show Optional Product', default=True, copy=True)
    page_break_after_optional_product = fields.Boolean('Page break after optional product', default=False, copy=True)

    #
    # _onchange methods
    #
    @api.onchange('pretext_id')
    def _onchange_pretext(self):
        converted_text = self._get_converted_text(self.pretext_id.pretext)
        self.pretext = converted_text

    @api.onchange('terms_and_conditions_id')
    def _onchange_terms_and_conditions(self):
        converted_text = self._get_converted_text(self.terms_and_conditions_id.terms_and_conditions)
        self.terms_and_conditions = converted_text

    @api.onchange('confirmation_letter_id')
    def _onchange_confirmation_letter(self):
        converted_text = self._get_converted_text(self.confirmation_letter_id.template)
        self.confirmation_letter = converted_text

    #
    # _compute methods
    #
    @api.depends('order_line.discount_amount')
    def _compute_discount_total(self):
        for order in self:
            order.discount_total = sum(order.order_line.mapped('discount_amount'))

    @api.depends('order_line.tax_id', 'order_line.price_unit', 'amount_total', 'amount_untaxed')
    def _compute_tax_totals_json(self):
        super()._compute_tax_totals_json()
        for rec in self:
            tax_totals_json_dict = json.loads(rec.tax_totals_json)
            tax_totals_json_dict.update({
                'discount_total': rec.discount_total,
                'formatted_discount_total': formatLang(self.env, rec.discount_total * -1.0, currency_obj=rec.currency_id),
                'amount_undiscounted': rec.amount_undiscounted,
                'formatted_amount_undiscounted': formatLang(self.env, rec.amount_undiscounted, currency_obj=rec.currency_id),
            })
            rec.tax_totals_json = json.dumps(tax_totals_json_dict)

    @api.depends('order_line')
    def get_subtotal_group_by_section(self):
        res = {}
        sub_total = 0
        for line in reversed(self.order_line):
            if line.display_type not in ('line_section', 'line_note'):
                sub_total += line.price_subtotal
            else:
                res[line.id] = sub_total
                sub_total = 0
        return res

    def _compute_amount_undiscounted(self):
        # override native func for adapting to the new discount policy
        for rec in self:
            rec.amount_undiscounted = rec.amount_untaxed + rec.discount_total

    def _compute_l10n_de_template_data_inherit(self):
        for record in self:
            record.l10n_de_template_data_inherit = data = []
            if record.partner_id.ref:
                data.append((_("Kundennr"), record.partner_id.ref))
            if record.date_order:
                data.append((_("Auftragsdatum"), format_date(self.env, record.date_order)))
            if record.state in ('draft', 'sent'):
                if record.validity_date:
                    data.append((_("Expiration"), format_date(self.env, record.validity_date)))
            if record.user_id:
                data.append((_("Berater"), record.user_id.name))
            if record.partner_id.phone:
                data.append((_("Tel."), record.partner_id.email))
            if record.partner_id.email:
                data.append((_("E-Mail"), record.partner_id.email))
            if 'incoterm' in record._fields and record.incoterm:
                data.append((_("Incoterm"), record.incoterm.code))

    #
    # action button
    #

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            order.write({'name': order.name.replace('AN', 'AB')})
        return res

    def action_cancel(self):
        res = super().action_cancel()
        for order in self:
            order.write({'name': order.name.replace('AB', 'AN')})
        return res

    #
    # other logic methods
    #

    def _get_converted_text(self, html):
        def _get_object_attribute(match):
            object = self
            try:
                object = eval(match.group(0))
                if not isinstance(object, (str, int, float, date, datetime, bool)):
                    object = object.display_name
            except Exception:
                object = "N/A"
            return str(object)

        converted_text = html
        if html:
            pattern = "[^{\}]+(?=})"
            converted_text = re.sub(pattern, _get_object_attribute, html)
            converted_text = re.sub(r"[{}]", '', converted_text)

        return converted_text


class SaleOrderTemplatePretext(models.Model):
    _name = 'sale.order.template.pretext'
    _description = 'Quotation / Order Template Pretext'

    name = fields.Char('Template Name', required=True)
    pretext = fields.Html(string='Pre Text')
    pretext_preview = fields.Html(string='Pre Text Preview', compute='_compute_pretext_preview', store=True)

    @api.depends('pretext')
    def _compute_pretext_preview(self):
        for record in self:
            if record.pretext:
                if len(record.pretext) > 50:
                    record.pretext_preview = '%s...' % record.pretext[0:50]
                else:
                    record.pretext_preview = record.pretext
            else:
                record.pretext_preview = False


class SaleOrderTemplateTermsAndConditions(models.Model):
    _name = 'sale.order.template.terms.and.conditions'
    _description = 'Quotation / Order Template Post Text'

    name = fields.Char('Template Name', required=True)
    terms_and_conditions = fields.Html(string='Post Text')
    terms_and_conditions_preview = fields.Html(string='Post Text Preview', compute='_compute_post_text_preview',
                                               store=True)

    @api.depends('terms_and_conditions')
    def _compute_post_text_preview(self):
        for record in self:
            if record.terms_and_conditions:
                if len(record.terms_and_conditions) > 50:
                    record.terms_and_conditions_preview = '%s...' % record.terms_and_conditions[0:50]
                else:
                    record.terms_and_conditions = record.terms_and_conditions
            else:
                record.terms_and_conditions = False


class SaleOrderConfirmationLetter(models.Model):
    _name = 'sale.order.confirmation.letter'
    _description = 'Sale Order Confirmation Letter'

    name = fields.Char(string='Name', required=True)
    template = fields.Html(string='Template')
