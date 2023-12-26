{
    'name': "Product Kits Addons",
    'summary': "Product Kits Management Addons",
    'version': '15.0.1.0.0',
    'author': "simplify-m110",
    'category': 'Sales',
    'website': 'https://simplify-erp.com',
    'license': 'LGPL-3',
    'depends': ['base','product','product_kits-main'],
    'data': [
        #data
        "data/ir_access.xml",
        "data/automatic_action.xml",

        # security
        # 'security/ir.model.access.csv',

        # views
        'views/x_product_template.xml',
        'views/x_res_config_settings_views.xml',

    ],
    # 'assets': {
    #     'web.assets_frontend': [
    #         'product_kits-addons/static/src/js/x_website_sale.js',
    #     ],
    # },
    'auto_install': False,
    'installable': True,
}
