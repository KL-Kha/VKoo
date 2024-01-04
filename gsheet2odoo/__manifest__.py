{
    'name': "Google Sheets Importer",
    'version': '1.0',
    'author': "(initially) Ashant Chalasani",
    'company': "PowerOn | Wapsol GmbH",
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings.xml',
    ],
    # 'external_dependencies': {
    #     'python': ['pandas','gspread', 'oauth2client'],
    # },
}
