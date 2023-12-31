import logging

from odoo import fields, models, api, _
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class FlashlistData(models.Model):
    _name = 'flashlist.data'
    _description = 'Flashlist Data import from manufacturer'

    name = fields.Char(compute='_compute_name')
    article_number = fields.Char()
    article_description = fields.Char()
    manufacturer = fields.Char()
    performance = fields.Char()
    serial_number = fields.Char()
    pallet_number = fields.Char()
    container_number = fields.Char()
    order_number = fields.Char()
    pmpp = fields.Char()
    umpp = fields.Char()
    impp = fields.Char()
    vmpp = fields.Char()
    isc = fields.Char()
    uoc = fields.Char()
    voc = fields.Char()
    attachment_id = fields.Many2one(comodel_name='ir.attachment')
    product_id = fields.Many2one(comodel_name='product.product')
    serial_number_optimizer = fields.Char()

    @api.depends('attachment_id')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.attachment_id.name or 'N/A'

    def add_product_supplier(self):
        # Init variables
        partner_env = self.env['res.partner']

        # Create supplier (manufacturer) if not exists
        manufacturer = self.manufacturer
        partner = partner_env.search([('name', '=', manufacturer), ('company_type', '=', 'company')], limit=1)
        partner = partner or partner_env.create({'name': manufacturer, 'company_type': 'company'})

        # Search if supplier info exists
        product_supplier = self.product_id.seller_ids.filtered(lambda s: s.name == partner and s.article_no == self.article_number)

        if not product_supplier:
            vals = {
                'name': partner.id,
                'product_id': self.product_id.id,
                'flashlist_file_id': self.attachment_id.id,
                'article_no': self.article_number,
                'product_name': self.article_description,
                'delay': 0,
            }
            self.product_id.write({'seller_ids': [(0, 0, vals)]})

    def remove_product_supplier(self):
        supplier = self.product_id.seller_ids.filtered(lambda s: s.flashlist_file_id == self.attachment_id)
        if supplier:
            supplier.unlink()
