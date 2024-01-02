# -*- coding: utf-8 -*-
{
    'name': "Merge Issues",

    'summary': """
        Merge issues""",

    'description': """
        This module will be used to merge multiple issues into one
    """,

    'author': "Cona Cons (RISTE KABRANOV)",
    'website': "http://www.euroblaze.de",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Administration',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project','project_issue', 'project_issue_sheet'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
