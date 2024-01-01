{
    'name': 'Poweron Flashlist',
    'version': '1.0',
    'license': 'AGPL-3',
    'author': 'Simplify m97',
    'company': 'SimplifyERP',
    'website': 'https://simplify-erp.com/',
    'depends': ['base', 'stock'],
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Views
        'views/flashlist_views.xml',
        'views/stock_move_views.xml',
        'views/stock_prod_lot_views.xml',
    ],

    'installable': True,
    'auto_install': False,
}
