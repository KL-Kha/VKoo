# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class SaleProductConfiguratorWizard(models.TransientModel):
    _inherit = 'sale.product.configurator'

    def product_configurator(self):
        context = self._context
        wizard_id = False
        if context.get('bundle_wizard_id'):
            wizard_id = context['bundle_wizard_id']
            if context.get('bundle_line_id'):
                bundle_line_id = self.env['add.bundle.wizard.line'].browse(context.get('bundle_line_id'))
                if bundle_line_id:
                    if context.get('product_id'):
                        product_id = self.env['product.product'].browse(context.get('product_id'))
                        quantity = context.get('quantity') if context.get('quantity') else False
                        bundle_line_id.write({'product_kit_product_id': product_id.id,
                                              'quantity_per_product': quantity,
                                              'product_uom': product_id.uom_id.id})

        return wizard_id
