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
        df = pd.read_excel(excel_path, header=None, skiprows=7, usecols=[0, 1, 3, 4, 9, 11])
        for index, row in df.iterrows():
            kunden_nr = row[0]
            if type(kunden_nr) == float:
                kunden_nr = ''
            matchcode = row[1]
            if type(matchcode) == float:
                matchcode = ''
            Name = row[3]
            if type(Name) == float:
                Name = ''
            Vorname = row[4]
            if type(Vorname) == float:
                Vorname = '' 
            Strasse = row[9]
            if type(Strasse) == float:
                Strasse = ''
            Telefon = row[11]
            if type(Telefon) == float:
                Telefon = ''

            if Name and Vorname:
                name_vorname = Name + ', ' + Vorname
            elif Name:
                name_vorname = Name
            elif Vorname:
                name_vorname = Vorname

            ref_customer = 'C' + str(kunden_nr)

            # Define a list to store search results
            search_results = []

            # Add search results to the list
            if matchcode:
                res_partner_matchcode_ids = self.env['res.partner'].search([('name', 'ilike', matchcode)])
                search_results.append(res_partner_matchcode_ids)

            if Name:
                res_partner_name_ids = self.env['res.partner'].search([('name', 'ilike', Name)])
                search_results.append(res_partner_name_ids)

            if name_vorname:
                res_partner_name_vorname_ids = self.env['res.partner'].search([('name', 'ilike', name_vorname)])
                search_results.append(res_partner_name_vorname_ids)

            if Strasse:
                res_partner_strasse_ids = self.env['res.partner'].search(['|', ('street', 'ilike', Strasse), ('street2', '=', Strasse)])
                search_results.append(res_partner_strasse_ids)

            if Telefon:
                res_partner_telefon_ids = self.env['res.partner'].search(['|', ('phone', 'ilike', Telefon), ('mobile', 'ilike', Telefon)])
                search_results.append(res_partner_telefon_ids)

            # Filter out empty search results
            non_empty_search_results = [result for result in search_results if len(result) > 0]
            if non_empty_search_results:
                common_records = set.intersection(*map(set, non_empty_search_results))
                common_records_list = list(common_records)

                if len(common_records) == 1:
                    common_records_list[0].write({
                        'ref': ref_customer
                    })