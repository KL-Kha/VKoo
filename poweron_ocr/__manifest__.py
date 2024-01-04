{
    "name": "Poweron OCR",
    "summary": "Poweron OCR bill digitalization",
    "author": "Simplify ERP",
    "website": "https://poweron.software",
    "version": "15.0.1.0.1",
    "license": "AGPL-3",
    "depends": ["account", "purchase"],
    "data": [
        # security
        "security/ir.model.access.csv",
        # views
        "views/account_move.xml",
        "views/purchase_order.xml",
        "views/res_config_settings.xml",
    ],
    "external_dependencies": {"python": ["google-cloud-documentai"]},
    "application": False,
}
