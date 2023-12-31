import os
import json
from google.cloud import documentai
from google.api_core.client_options import ClientOptions

from odoo import models, fields, api, tools, _
from odoo.osv import expression
from odoo.exceptions import ValidationError
from dateutil.parser import parse


class OCRMixin(models.AbstractModel):
    _name = 'ocr.mixin'
    _description = 'Handle extract pdf data with OCR'

    ocr_status = fields.Selection(selection=[
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('none', 'N/A'),
    ], default='none')

    LIST_SYMBOL = ['€', '$', 'د.إ', 'Afs', 'L', 'դր.', 'ƒ', 'Kz', '$', '$', 'Afl.', 'm', 'KM', 'Bds$', '৳', 'лв', 'BD', 'FBu', 'BD$', '$', 'Bs.', 'R$', 'B$', 'Nu.', 'P', 'Br', 'BR', 'BZ$', '$', 'Fr', 'CHF', '$', '$', '¥', '¥', '$', '$', '$', 'Kč', 'Fdj', 'kr', 'RD$', 'DA', 'E£', 'Nfk', 'Br', 'FJ$', '£', '£', 'ლ', 'GH¢', '£', 'D', 'FG', 'Q', '$', '$', 'L', 'kn', 'G', 'Ft', 'Rp', '₪', '₹', ' ع.د', '﷼', 'kr', '$', ' د.ا ', '¥', 'KSh', 'лв', '៛', 'CF', '₩', '₩', ' د.ك ', '$', 'лв', '₭', 'ل.ل', 'Rs', 'L$', 'M', 'Lt', 'Ls', ' ل.د ', 'DH', 'L', 'Ar', 'ден', 'K', '₮', 'MOP$', 'UM', 'UM', 'Rs', '.ރ', 'MK', '$', 'RM', 'MT', '$', '₦', 'C$', 'kr', '₨', '$', 'ر.ع.', 'B/.', 'S/', 'K', '₱', 'Rs.', 'zł', '₲', 'QR', 'lei', 'din.', 'руб', 'RF', 'SR', 'SI$', 'SR', 'ج.س.', 'kr', 'S$', '£', 'Le', 'Sh.', '$', '£', 'Db', 'Db', '¢', '£', 'E', '฿', 'TJS', 'T', 'DT', 'T$', '₺', '$', 'NT$', 'TSh', '₴', 'USh', '$', '$', '$', 'лв', 'Bs.F', 'Bs', '₫', 'VT', 'WS$', 'FCFA', '$', 'CFA', 'XPF', '﷼', 'R', 'ZK', 'Z$']

    ocr_data = fields.Text()
    default_ocr_product_id = fields.Many2one(comodel_name='product.product')
    default_ocr_partner_id = fields.Many2one(comodel_name='res.partner')

    def get_object_data_vals(self, document):
        partner_data = {
            'company_type': 'company',
            'supplier_rank': 1,
        }
        line_ids = [(5, 0, 0)]
        object_data = {}
        ocr_data = {}
        ocr_line_number = 1

        ocr_object_mapping = self._get_ocr_object_mapping()
        ocr_partner_mapping = self._get_ocr_partner_mapping()
        ocr_object_line_mapping = self._get_ocr_object_line_mapping()

        for entity in document.entities:
            key = entity.type_
            ocr_data.update({
                key: entity.normalized_value.text or entity.text_anchor.content
            })
            if key in ocr_object_mapping.keys():
                value = entity.normalized_value.text or entity.text_anchor.content
                if key == 'sale_person':
                    value = self.env['res.users'].search([('name','ilike',entity.normalized_value.text or entity.text_anchor.content)],limit=1)
                    if not value:
                        continue
                if key == 'pre_text':
                    vals = {
                        'name': self.name,
                        'pretext':value,
                    }
                    pretext_id = self.env['sale.order.template.pretext'].create(vals)
                    value = pretext_id.id
                if 'date' in key:
                    value = self.get_date(value)
                field_name = ocr_object_mapping.get(key)
                object_data.update({field_name: value})

            if key in ocr_partner_mapping.keys():
                value = entity.normalized_value.text or entity.text_anchor.content
                field_name = ocr_partner_mapping.get(key)
                # remove spaces in vat number
                if field_name == 'vat':
                    value = value.replace(" ", "")
                partner_data[field_name] = value

            # overall vat parsing
            if key == 'vat':
                for i in range(0, len(entity.properties)):
                    col = entity.properties[i]
                    line_val = col.normalized_value.text or col.text_anchor.content
                    if not ocr_data.get('vat'):
                        ocr_data.update({'vat': [line_val]})
                    else:
                        ocr_data['vat'].append(line_val)

            # object lines parsing
            if key == 'line_item' and ocr_object_line_mapping:
                vals = {}
                for i in range(0, len(entity.properties)):
                    col = entity.properties[i]
                    if col.text_anchor.content in self.LIST_SYMBOL:
                        continue
                    ocr_data.update({
                        f"{col.type_}_{ocr_line_number}": col.normalized_value.text or col.text_anchor.content
                    })
                    line_key = ocr_object_line_mapping.get(col.type_)
                    if line_key:
                        line_val = col.normalized_value.text or col.text_anchor.content
                        line_val = self._optimize_val(line_key, line_val)
                        vals.update({line_key: line_val})

                # Apply 19% as default Tax if configuration is set
                list_tax_name = ocr_data.get('vat', '')
                if list_tax_name and ocr_object_line_mapping.get('line_item/tax'):
                    if self.company_id.is_dokuscan_overall_tax:
                        list_tax_name = ['19']
                    tax_key = ocr_object_line_mapping.get('line_item/tax')
                    vals.update({tax_key: self._get_tax_vals(list_tax_name)})
                vals.update
                line_ids.append((0, 0, vals))
                ocr_line_number += 1

        object_data.update({'ocr_data': json.dumps(ocr_data, indent=4)})

        # partner parsing
        partner_id = self._prepare_partner_data(partner_data)
        if partner_id:
            object_data.update({'partner_id': partner_id})

        object_line_key = self._get_object_line_key()
        if object_line_key:
            line_ids = self._assign_line_product(line_ids)
            object_data.update({object_line_key: line_ids})

        return object_data

    @api.model
    def _prepare_documentai_auth(self, **kwargs):
        try:
            gg_project_id = tools.config['gg_project_id']
            gg_location = tools.config['gg_location']
            if self._name == 'sale.order':
                gg_processor_id = tools.config['gg_processor_id_so']
            else:
                gg_processor_id = tools.config['gg_processor_id']
            gg_mime_type = tools.config['gg_mime_type']
            gg_default_auth_path = tools.config['gg_default_auth_path']
        except Exception as err:
            raise ValidationError(_("You need to set values for documentai (DokuScan) in the PowerOn™ configuration file.")) from err
        return gg_project_id, gg_location, gg_processor_id, gg_mime_type, gg_default_auth_path

    @staticmethod
    def get_date(string, fuzzy=True):
        """
        Return date interpreted from string.
        Return false when date cannot be converted

        :param string: str, string to check for date
        :param fuzzy: bool, ignore unknown tokens in string if True
        """
        try:
            return parse(string, fuzzy=fuzzy)
        except Exception:
            return False

    def update_send_ocr_status(self, success=True, reason=''):
        msg = ""
        if success:
            msg = f"Succeed sending document '{self.message_main_attachment_id.name}' for Digitalization."
            self.ocr_status = 'success'
        else:
            msg = f"There is an error when Sending for Digitalization.\n\nDetails: {reason}"
            self.ocr_status = 'failed'
        self.message_post(body=msg)

    def ocr_send(self):
        project_id, location, processor_id, mime_type, default_auth_path = self._prepare_documentai_auth()

        for object in self:
            attachment = object.message_main_attachment_id
            if not attachment:
                raise ValidationError(_("Please attach a document to send for digitalization"))
            if object.state not in ['draft']:
                raise ValidationError(_("Send for Digitalization applies only on draft state"))
            try:
                # prepare connection to document googleapis
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = default_auth_path
                opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
                client = documentai.DocumentProcessorServiceClient(client_options=opts)
                name = client.processor_path(project_id, location, processor_id)
                raw_document = documentai.RawDocument(content=attachment.raw, mime_type=mime_type)

                # proceed file and get result
                request = documentai.ProcessRequest(name=name, raw_document=raw_document)
                result = client.process_document(request=request)
                document = result.document

                # parse data to odoo object
                vals = object.get_object_data_vals(document)
                object.write(vals)
                object.update_send_ocr_status(success=True)
            except Exception as e:
                object.update_send_ocr_status(success=False, reason=str(e))

    def _optimize_val(self, key, val):
        result = val
        if 'tax' in key:
            result = self._get_tax_vals([val])
        elif 'name' not in key:
            for token in val.split():
                token = token.replace(',', '.')
                if token.replace('.', '').isdigit():
                    result = token
                    break
        return result

    def _get_tax_vals(self, list_tax_name):
        tax_ids = []
        for tax_name in list_tax_name:
            tax = self.env['account.tax'].search([('name', 'ilike', tax_name)], limit=1)
            if not tax:
                msg = _(f"Cannot find tax {tax_name} in the system")
                self.message_post(body=msg)
                continue
            tax_ids.append(tax.id)
        return [(6, 0, tax_ids)]

    def _prepare_partner_data(self, partner_data):
        partner = self.env['res.partner']
        bank_env = self.env['res.partner.bank']
        for field, operator in self._get_partner_search_fields().items():
            field_val = partner_data.get(field)
            if field_val:
                domain = [(field, operator, field_val)]
                if operator == 'ilike':
                    domain = [(field, operator, '%'+ field_val +'%')]
                partner = partner.search(domain, limit=1)
            if partner:
                partner.vat = partner.vat or partner_data.get('vat')
                break

        if not partner:
            partner_data.update({'company_type': 'company'})
            if partner_data.get('name'):
                partner = partner.create(partner_data)
            else:
                partner = self.default_ocr_partner_id

        # prepare partner's bank
        iban = partner_data.get('iban') and partner_data.pop('iban') or False
        bank_exist = partner.bank_ids.filtered(lambda b: b.acc_number == iban)
        if not bank_exist and iban:
            bank_vals = {
                'acc_number': iban,
                'partner_id': partner.id,
                'company_id': self.company_id.id
            }
            bank_env.create(bank_vals)

        return partner.id or False

    def _assign_line_product(self, line_ids):
        object_line_ids = line_ids
        for i, line in enumerate(line_ids[1:]):
            line_name = line[2].get('name', '')
            line_name.replace("\n", " ")
            product_id = self.env['product.product'].search([('name', 'ilike', line_name)], limit=1)
            if self._name == 'sale.order':
                object_line_ids[i + 1][2].update({'product_id': product_id.id or self.default_ocr_product_id.id})
            else:
                object_line_ids[i + 1][2].update({'product_id': product_id.id or self.default_ocr_product_id.id})
        return object_line_ids

    def _get_partner_search_fields(self):
        # return field_name and search_operator
        return {
            'vat': '=',     # exact search
            'email': '=',     # exact search
            'name': 'ilike'     # fuzzy search
        }

    def _get_ocr_partner_mapping(self):
        return {
            'supplier_name': 'name',
            'supplier_phone': 'phone',
            'supplier_email': 'email',
            'supplier_website': 'website',
            'supplier_address': 'street',
            'supplier_tax_id': 'vat',
            'supplier_iban': 'iban',
        }

    def _get_ocr_object_mapping(self):
        return {}

    def _get_ocr_object_line_mapping(self):
        return {}

    def _get_object_line_key(self):
        return ''