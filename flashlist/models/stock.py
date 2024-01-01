from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = 'stock.move'

    use_flashlist = fields.Boolean(compute='_compute_use_flashlist', readonly=False)
    flashlist_id = fields.Many2one(comodel_name='ir.attachment')
    allowed_flashlist_ids = fields.Many2many(comodel_name='ir.attachment', compute='_compute_allowed_flashlist_ids')

    @api.depends('picking_type_id')
    def _compute_use_flashlist(self):
        for rec in self:
            use_flashlist = False
            if rec.picking_type_id.sequence_code == 'IN':
                use_flashlist = True
            rec.use_flashlist = use_flashlist

    def _compute_allowed_flashlist_ids(self):
        flashlists = self.env['flashlist.data'].search([('product_id', '!=', False)])
        attachments = flashlists.mapped('attachment_id').ids
        for rec in self:
            rec.allowed_flashlist_ids = [(6, 0, attachments)]

    def action_assign_serial_show_details(self):
        # overwrite native func to have flashlist functionality
        ctx = self._context.copy()
        if self.use_flashlist:
            self.next_serial = '1'  # preserver for not being catched by odoo native checks
            ctx.update({
                'use_flashlist': self.flashlist_id.id,
                'product_flashlist_id': self.product_id.id,
            })
        return super(StockMove, self.with_context(ctx)).action_assign_serial_show_details()

    def action_clear_lines_show_details(self):
        res = super().action_clear_lines_show_details()
        if self.use_flashlist:
            flashlists = self.env['flashlist.data'].search([
                ('attachment_id', '=', self.flashlist_id.id), ('product_id', '!=', False)])
            if flashlists:
                flashlists[0].remove_product_supplier()
                flashlists.write({'product_id': False})
        return res


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    flashlist_data_id = fields.Many2one(comodel_name='flashlist.data', compute='_compute_flashlist_data_id', store=True)
    pallet_number = fields.Char(related='flashlist_data_id.pallet_number', store=True)
    article_number = fields.Char(related='flashlist_data_id.article_number', store=True)
    article_description = fields.Char(related='flashlist_data_id.article_description', store=True)
    manufacturer = fields.Char(related='flashlist_data_id.manufacturer', store=True)
    performance = fields.Char(related='flashlist_data_id.performance', store=True)
    pmpp = fields.Char(related='flashlist_data_id.pmpp', store=True)
    umpp = fields.Char(related='flashlist_data_id.umpp', store=True)
    vmpp = fields.Char(related='flashlist_data_id.vmpp', store=True)
    impp = fields.Char(related='flashlist_data_id.impp', store=True)
    isc = fields.Char(related='flashlist_data_id.isc', store=True)
    uoc = fields.Char(related='flashlist_data_id.uoc', store=True)
    voc = fields.Char(related='flashlist_data_id.voc', store=True)

    @api.depends('name', 'product_id')
    def _compute_flashlist_data_id(self):
        flashlist_data = self.env['flashlist.data'].search([
            ('serial_number', 'in', self.mapped('name')),
            ('product_id', 'in', self.mapped('product_id').ids),
        ])
        for rec in self:
            data_id = flashlist_data.filtered(lambda f: f.product_id == rec.product_id and f.serial_number == rec.name) or False
            rec.flashlist_data_id = data_id

    @api.model
    def generate_lot_names(self, first_lot, count):
        flashlist_atch_id = self._context.get('use_flashlist', False)
        if flashlist_atch_id:
            product_id = self._context.get('product_flashlist_id', False)
            flashlists = self.env['flashlist.data'].search([
                ('attachment_id', '=', flashlist_atch_id), ('product_id', '=', False)])
            if not flashlists:
                raise ValidationError(_("All the Serial Numbers in Flashlist have been assigned"))

            # mark flashlist as proceeded
            flashlists.write({'product_id': product_id})
            flashlists[0].add_product_supplier()
            return flashlists.mapped('serial_number')
        return super().generate_lot_names(first_lot, count)

    @api.model
    def _get_next_serial(self, company, product):
        if self._context.get('use_flashlist', False):
            return False
        return super()._get_next_serial(company, product)


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    flashlist_file_id = fields.Many2one(comodel_name='ir.attachment')
