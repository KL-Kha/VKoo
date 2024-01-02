from odoo import models


class Import(models.TransientModel):
    _inherit = 'base_import.import'

    def execute_import(self, fields, columns, options, dryrun=False):
        res = super().execute_import(fields, columns, options, dryrun)
        if not dryrun and self.res_model == 'flashlist.data':
            attachment = self.env['ir.attachment'].create({
                'name': self.file_name,
                'type': 'binary',
                'raw': self.file,
            })
            imported_flashlists = self.env['flashlist.data'].browse(res.get('ids'))
            imported_flashlists.write({'attachment_id': attachment.id})
        return res
