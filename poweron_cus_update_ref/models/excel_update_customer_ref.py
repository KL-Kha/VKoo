from odoo import api, fields, models, _
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
from odoo.exceptions import ValidationError
from urllib.parse import urlparse, parse_qs
import pandas as pd
import re

_logger = logging.getLogger(__name__)


class ExcelUpdateCustomerRef(models.Model):
    _name = 'excel.update.customer.ref'

    @api.model
    def get_google_sheet_data(self):

        excel_path = self.env.user.company_id.excel_path
        df = pd.read_excel(excel_path, header=None, skiprows=7, usecols=[0, 1])
        for index, row in df.iterrows():
            kunden_nr = row[0]
            matchcode = row[1]

            ref_customer = 'c'+ str(kunden_nr)

            res_partner_match_ids = self.env['res.partner'].search([('name','ilike',matchcode)])
            if len(res_partner_match_ids) > 1:
                raise ValidationError(_("Have found more than 1 match Partner with name: %s and id: %s" %(matchcode,kunden_nr)))
            else:
                res_partner_match_ids.write({
                    'ref': ref_customer
                })

