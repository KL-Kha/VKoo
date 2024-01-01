from odoo import models


class Import(models.TransientModel):
    """
    This class extends the functionality of the base_import.import model in Odoo.
    It is designed to handle the specific case of importing 'flashlist.data' records.
    The purpose is to ensure that when flashlist data is imported, it not only creates 
    the flashlist data records but also links them with the corresponding file attachments 
    for future reference and traceability.
    """
    _inherit = 'base_import.import'

    def execute_import(self, fields, columns, options, dryrun=False):
        """
        Executes the import process with additional handling for 'flashlist.data'. 

        First, it calls the super method to perform the standard import operation. If the import
        is not a dry run and the model being imported is 'flashlist.data', it then creates a new 
        attachment record for the imported file. This attachment is linked to each imported 
        flashlist data record, ensuring that the source file of the import is traceable and 
        accessible in the future.

        :param fields: List of fields being imported.
        :param columns: List of columns in the import file.
        :param options: Import options (e.g., encoding, separator).
        :param dryrun: Boolean indicating if this is a trial run (True) or actual import (False).
        :return: The result of the import operation.
        """
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
