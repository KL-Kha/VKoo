{
    "name": "Website Sale Customization",
    "version": "16.0.1.0.0",
    "category": "Website",
    "author": "Poweron Software",
    "license": "AGPL-3",
    "summary": "Adjust content on website sale",
    "depends": ["website","website_sale"],
    "data": [
        "data/ir_asset.xml",
        "views/website_sale_template.xml",
    ],
    'assets': {
        'web.assets_editor': [
            ('replace', 'website/static/src/components/ace_editor/ace_editor.js', 'poweron_website_sale/static/src/js/ace_editor.js'),
        ],
    },
    
    "installable": True,
}
