# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def add_bundle(self):
        context = {'default_sale_order_id': self.ids[0]}
        return {
            'name': 'Add Bundle',
            'domain': [],
            'context': context,
            'res_model': 'add.bundle.wizard',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }
