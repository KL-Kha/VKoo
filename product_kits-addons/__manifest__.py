{
    'name': "Product Kits Addons",
    'summary': "Product Kits Management Addons",
    'version': '16.0.1.0.0',
    'author': "simplify-m110",
    'category': 'Sales',
    'website': 'https://simplify-erp.com',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        #data
        "data/automatic_action.xml",

        # security
        # 'security/ir.model.access.csv',

        # views
        'views/x_product_template.xml',
        'views/x_res_config_settings_views.xml',

    ],
    'auto_install': False,
    'installable': True,
}
