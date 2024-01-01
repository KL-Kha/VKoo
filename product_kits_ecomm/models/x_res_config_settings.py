# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import literal_eval

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    x_anfrage_modus_mode = fields.Boolean(string='Anfrage Modus / RFQ Mode',related='company_id.x_anfrage_modus_mode', readonly=False)