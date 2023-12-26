# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class AddBundleWizard(models.TransientModel):
    _name = 'add.bundle.wizard'
    _description = 'Add Bundle'

    kit_template_id = fields.Many2one('product.template', string='Bundle', domain="[('product_pack', '=', True)]")
    quantity_per_products = fields.Float('Quantity', default=0.0, store=True)
    product_line_kit_ids = fields.One2many('add.bundle.wizard.line', 'wizard_id', )
    sale_order_id = fields.Many2one('sale.order')
    sale_order_template_id = fields.Many2one('sale.order.template')

    @api.onchange('quantity_per_products')
    def onchange_quantity_per_products(self):
        if self.quantity_per_products:
            for line in self.product_line_kit_ids:
                line.quantity_per_product = self.quantity_per_products * line.line_id.quantity_per_product
        else:
            for line in self.product_line_kit_ids:
                line.quantity_per_product = 0.0

    @api.onchange('kit_template_id')
    def on_change_kit_template_id(self):
        if self.kit_template_id:
            self.quantity_per_products = 1
            line_ids = self.env['add.bundle.wizard.line']
            for product_line in self.kit_template_id.product_line_kit_ids:
                line = {
                    'wizard_id': self.id,
                    'quantity_per_product': product_line.quantity_per_product,
                    'product_kit_template_id': product_line.product_kit_template_id.id,
                    'line_id': product_line.id,
                }
                products = self.env['product.product'].search(
                    [('product_tmpl_id', '=', product_line.product_kit_template_id.id)]
                )
                if len(products) == 1:
                    line.update({'product_kit_product_id': products.id,
                                 'product_uom': products.uom_id.id})
                line_ids |= self.env['add.bundle.wizard.line'].create(line)

                self.product_line_kit_ids = [(5, 0, 0)] + [(6, 0, line_ids.ids)]
        else:
            self.quantity_per_products = 0
            self.product_line_kit_ids = [(5, 0, 0)]

    def add_bundle(self):
        for wizard in self:
            if wizard.sale_order_id:
                for line in wizard.product_line_kit_ids:
                    if line.product_kit_product_id:
                        vals = {
                            'product_id': line.product_kit_product_id.id,
                            'product_uom_qty': line.quantity_per_product * (wizard.quantity_per_products or 1),
                            'product_uom': line.product_uom.id,
                            'order_id': wizard.sale_order_id.id
                        }
                        self.env['sale.order.line'].create(vals)
            if wizard.sale_order_template_id:
                for line in wizard.product_line_kit_ids:
                    if line.product_kit_product_id:
                        vals = {'product_id': line.product_kit_product_id.id,
                                'product_uom_qty': line.quantity_per_product * (wizard.quantity_per_products or 1),
                                'product_uom_id': line.product_uom.id,
                                'sale_order_template_id': wizard.sale_order_template_id.id,
                                'name': line.product_kit_product_id.get_product_multiline_description_sale()
                                }
                        self.env['sale.order.template.line'].create(vals)


class SaleBundleLineWizard(models.TransientModel):
    _name = 'add.bundle.wizard.line'
    _description = 'Add Bundle Wizard Line'

    quantity_per_product = fields.Float('Quantity', default=0.0, store=True)
    product_kit_template_id = fields.Many2one('product.product', string='Product')
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure')
    product_kit_product_id = fields.Many2one('product.product')
    available_product_kit_product_ids = fields.Many2many('product.product', string='Product Variant',
                                                         compute='_compute_available_product_kit_product_ids')
    wizard_id = fields.Many2one('add.bundle.wizard')
    line_id = fields.Many2one('product.kit.line')

    @api.depends('product_kit_template_id')
    def _compute_available_product_kit_product_ids(self):
        for line in self:
            if line.product_kit_template_id:
                products = self.env['product.product'].search(
                    [('product_tmpl_id', '=', line.product_kit_template_id.id)]
                )
                line.available_product_kit_product_ids = products
                """if len(products) == 1:
                    line.product_kit_product_id = products.id
                    line.product_uom = products.uom_id.id"""
            else:
                line.available_product_kit_product_ids = False

    @api.onchange('product_kit_product_id')
    def _onchange_product_kit_product_id(self):
        if self.product_kit_product_id:
            self.update({'product_uom': self.product_kit_product_id.uom_id.id,
                         'quantity_per_product': self.wizard_id.quantity_per_products * self.line_id.quantity_per_product})
        else:
            self.update({'product_uom': False,
                         'quantity_per_product': self.wizard_id.quantity_per_products * self.line_id.quantity_per_product})
