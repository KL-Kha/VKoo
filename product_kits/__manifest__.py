{
    'name': "Product Kits",
    'summary': "Product Kits Management",
    'version': '16.0.1.0.0',
    'author': "simplify-m110",
    'category': 'Sales',
    'website': 'https://simplify-erp.com',
    'license': 'LGPL-3',
    'depends': ['base_setup', 'product', 'sale', 'sale_management'],
    'data': [
        # security
        'security/ir.model.access.csv',
        # wizard
        'wizard/add_bundle_wizard_views.xml',
        # 'wizard/sale_product_configurator_views.xml',
        # views
        'views/product_template.xml',
        'views/sale_order_views.xml',
        'views/sale_order_template_views.xml',

    ],
    'auto_install': False,
    'installable': True,
}
