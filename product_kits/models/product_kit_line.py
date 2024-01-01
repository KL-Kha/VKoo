# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ProductKitLine(models.Model):
    _name = 'product.kit.line'
    _description = 'Product Kit Line'

    product_template_id = fields.Many2one('product.template', string='Product Pack Ref.')
    product_kit_template_id = fields.Many2one('product.product', string='Product')
    quantity_per_product = fields.Float('Quantity', default=1.0)
    price = fields.Float(related="product_kit_template_id.list_price", store=True, string="Sale Price")
    cost = fields.Float(related="product_kit_template_id.standard_price", store=True, string="Purchase Price")
    price_total = fields.Float(compute="_compute_price_total", store=True)

    @api.depends('price', 'quantity_per_product')
    def _compute_price_total(self):
        for record in self:
            record.price_total = record.price * record.quantity_per_product
