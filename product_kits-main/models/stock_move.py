# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import fields, models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def create(self, vals):
        product = self.env['product.product'].search([('id', '=', vals['product_id'])])
        if product.product_pack:
            kit_products = product.product_line_kit_ids.filtered(
                lambda l: l.product_kit_template_id.detailed_type == 'product')
            res = None
            if kit_products:
                for kit_product in kit_products:
                    new_vals = vals
                    logging.info(vals)
                    quantity = vals['product_uom_qty']
                    if 'purchase_line_id' in vals:
                        line = self.env['purchase.order.line'].sudo().search([('id','=', int(vals['purchase_line_id']))],limit=1)
                        quantity = line.product_qty
                    elif 'sale_line_id' in vals:
                        line = self.env['sale.order.line'].sudo().search([('id','=', int(vals['sale_line_id']))],limit=1)
                        quantity = line.product_uom_qty
                    new_vals.update({
                        'product_id': kit_product.product_kit_template_id.id,
                        'product_uom_qty': quantity * kit_product.quantity_per_product
                    })
                    logging.info(vals)
                    logging.info(new_vals)
                    logging.info(vals['product_uom_qty'])
                    logging.info(kit_product.quantity_per_product)
                    if res:
                        res += super(StockMove, self).create(new_vals)
                    else:
                        res = super(StockMove, self).create(new_vals)
                return res
            else:
                return self.browse()
        elif product.detailed_type != 'product':
            return self.browse()
        else:
            res = super(StockMove, self).create(vals)
            return res