# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    discount_amount = fields.Monetary('Discount Amount', compute='_compute_line_discount_amount')

    @api.depends('product_uom_qty', 'price_unit')
    def _compute_line_discount_amount(self):
        for line in self:
            discount_amount = line.product_uom_qty * line.price_unit * line.discount / 100
            if line.price_subtotal < 0:
                discount_amount = abs(line.price_subtotal)
            line.discount_amount = discount_amount

    def _update_description(self):
        res = super()._update_description()
        if self.name and self.product_id.display_name in self.name:
            self.update({
                'name': self.name.replace(self.product_id.display_name, "").strip() + ' '
            })
        return res
