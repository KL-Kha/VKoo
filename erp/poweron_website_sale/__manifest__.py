{
    "name": "Website Sale Customization",
    "version": "16.0.1.0.0",
    "category": "Website",
    "author": "Poweron Software",
    "license": "AGPL-3",
    "summary": "Adjust content on website sale",
    "depends": ["website","website_sale"],
    "data": [
        "views/website_sale_template.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'poweron_website_sale/static/src/scss/user_custom_rules.scss',
        ],
    },
    "installable": True,
}
