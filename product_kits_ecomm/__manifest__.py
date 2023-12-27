{
    'name': "Product Kits Ecomm",
    'summary': "Product Kits Ecomm Management",
    'version': '16.0.1.0.0',
    'author': "simplify-m110",
    'category': 'Sales',
    'website': 'https://simplify-erp.com',
    'license': 'LGPL-3',
    'depends': ['base','base_automation','sale','website_sale','product','product_kits'],
    'data': [
        #data
        "data/ir_access.xml",
        "data/automatic_action.xml",

        # views
        'views/x_product_template.xml',
        'views/x_res_config_settings_views.xml',
        'views/website_sale_templates.xml',

    ],
    'auto_install': False,
    'installable': True,
}
