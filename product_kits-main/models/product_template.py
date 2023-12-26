# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_pack = fields.Boolean('Is Product Kit')
    product_line_kit_ids = fields.One2many('product.kit.line', 'product_template_id')
    kit_price = fields.Float('Kit Price', compute='_compute_kit_price', store=True)
    product_fixed_price = fields.Boolean('Fixed Price', default=False)

    @api.depends('product_line_kit_ids.price_total', 'product_pack')
    def _compute_kit_price(self):
        for res in self:
            if res.product_pack:
                sum_price = sum(res.product_line_kit_ids.mapped('price_total')) or 0
                res.kit_price = sum_price
                if not res.product_fixed_price:
                    res.list_price = sum_price
            else:
                res.kit_price = 0
