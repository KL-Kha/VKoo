from odoo import models, fields, api


class InvoiceTemplatePretext(models.Model):
    _name = 'invoice.template.pretext'
    _description = 'Invoice Template Pretext'

    name = fields.Char('Template Name', required=True)
    pretext = fields.Html(string='Pre Text')
    pretext_preview = fields.Html(string='Pre Text Preview', compute='_compute_pretext_preview', store=True)

    @api.depends('pretext')
    def _compute_pretext_preview(self):
        for record in self:
            if record.pretext:
                if len(record.pretext) > 50:
                    record.pretext_preview = '%s...' % record.pretext[0:50]
                else:
                    record.pretext_preview = record.pretext
            else:
                record.pretext_preview = False


class InvoiceTemplateTermsAndConditions(models.Model):
    _name = 'invoice.template.terms.and.conditions'
    _description = 'Invoice Template Post Text'

    name = fields.Char('Template Name', required=True)
    terms_and_conditions = fields.Html(string='Post Text')
    terms_and_conditions_preview = fields.Html(string='Post Text Preview', compute='_compute_post_text_preview',
                                               store=True)

    @api.depends('terms_and_conditions')
    def _compute_post_text_preview(self):
        for record in self:
            if record.terms_and_conditions:
                if len(record.terms_and_conditions) > 50:
                    record.terms_and_conditions_preview = '%s...' % record.terms_and_conditions[0:50]
                else:
                    record.terms_and_conditions = record.terms_and_conditions
            else:
                record.terms_and_conditions = False

