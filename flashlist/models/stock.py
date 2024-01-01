from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = 'stock.move'

    use_flashlist = fields.Boolean(compute='_compute_use_flashlist', readonly=False)
    flashlist_id = fields.Many2one(comodel_name='ir.attachment')
    allowed_flashlist_ids = fields.Many2many(comodel_name='ir.attachment', compute='_compute_allowed_flashlist_ids')

    @api.depends('picking_type_id')
    def _compute_use_flashlist(self):
        """
        Compute whether a flashlist should be used for the stock move. This is determined based on the picking
        type's sequence code. If the code is 'IN', indicating an incoming type, the flashlist is used. This
        method is necessary to automate the decision of using flashlist data in relevant stock move scenarios.
        """
        for rec in self:
            use_flashlist = False
            if rec.picking_type_id.sequence_code == 'IN':
                use_flashlist = True
            rec.use_flashlist = use_flashlist

    def _compute_allowed_flashlist_ids(self):
        """
        Compute the allowed flashlist IDs for a stock move. This method searches for all flashlist data
        linked to a product and lists their attachments. This allows the stock move to be associated only
        with relevant flashlist data, ensuring data integrity and relevance.
        """
        flashlists = self.env['flashlist.data'].search([('product_id', '!=', False)])
        attachments = flashlists.mapped('attachment_id').ids
        for rec in self:
            rec.allowed_flashlist_ids = [(6, 0, attachments)]

    def action_assign_serial_show_details(self):
        """
        Overwrite the native function to integrate flashlist functionality into the stock move's serial number
        assignment. This method modifies the context to include flashlist data when necessary, ensuring that
        serial numbers are assigned in accordance with flashlist details, enhancing data accuracy and traceability.
        """
        ctx = self._context.copy()
        if self.use_flashlist:
            self.next_serial = '1'  # preserver for not being catched by odoo native checks
            ctx.update({
                'use_flashlist': self.flashlist_id.id,
                'product_flashlist_id': self.product_id.id,
            })
        return super(StockMove, self.with_context(ctx)).action_assign_serial_show_details()

    def action_clear_lines_show_details(self):
        """
        Overwrite the native function to clear lines with flashlist integration. This method removes product
        supplier data linked to the flashlist when clearing stock move lines. It ensures that any cleanup
        of stock moves also accounts for the removal of associated supplier data, maintaining data consistency.
        """
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
    supplier = fields.Char(related='flashlist_data_id.supplier', store=True)
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
        """
        Compute the flashlist data ID for a stock production lot. This method links the production lot to the
        corresponding flashlist data based on the serial number and product ID. It ensures that each lot is
        correctly associated with its relevant flashlist data, facilitating detailed tracking and validation.
        """
        flashlist_data = self.env['flashlist.data'].search([
            ('serial_number', 'in', self.mapped('name')),
            ('product_id', 'in', self.mapped('product_id').ids),
        ])
        for rec in self:
            data_id = flashlist_data.filtered(lambda f: f.product_id == rec.product_id and f.serial_number == rec.name) or False
            rec.flashlist_data_id = data_id

    @api.model
    def generate_lot_names(self, first_lot, count):
        """
        Overrides the standard lot name generation method. In the context of using flashlists,
        this method ensures that lot names are derived from the serial numbers specified in the 
        flashlist. This approach maintains consistency between the flashlist data and the Odoo system, 
        ensuring accurate tracking of products as per the supplier's data.
        """
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
        """
        Customizes the generation of the next serial number in the context of using flashlists.
        If a flashlist is in use, this method prevents Odoo from automatically generating a serial 
        number, since the serial numbers are managed within the flashlist data.
        """
        if self._context.get('use_flashlist', False):
            return False
        return super()._get_next_serial(company, product)


class ProductSupplierinfo(models.Model):
    """
    This class extends the functionality of product.supplierinfo to link supplier information with 
    specific flashlists. The intention is to create a direct association between supplier records 
    and the flashlist data, allowing for enhanced traceability and supplier management based on 
    the imported flashlist information.
    """

    _inherit = "product.supplierinfo"

    flashlist_file_id = fields.Many2one(comodel_name='ir.attachment')
