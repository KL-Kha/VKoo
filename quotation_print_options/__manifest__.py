# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Print Options for Quotations and SaleOrders",
    'summary': "Customization on Sale Quotation/Order Template",
    'version': '15.0.1.0.0',
    'author': "Simplify-ERP™",
    'category': 'Sales',
    'website': 'https://simplify-erp.com',
    'license': 'LGPL-3',
    'depends': ["sale_management", "l10n_de"],
    'data': [
        # security
        'security/ir.model.access.csv',
        # views
        'views/sale_order_views.xml',
        'views/layouts.xml',
        # report
        'report/sale_report.xml',
        'report/sale_report_templates.xml',
        'report/sale_confirmation_report.xml',
        'report/footer.xml',
        # data
        'data/data.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            'quotation_print_options/static/src/xml/tax_totals_json.xml',
        ],
    },
    'auto_install': False,
    'installable': True,
}
