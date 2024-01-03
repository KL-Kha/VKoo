from odoo import tools
from odoo.api import Environment, SUPERUSER_ID

def main():
    with tools.config['workers']:
        registry = tools.odoo.modules.registry.Registry.new(tools.config['db_name'])
        with registry.cursor() as cr:
            env = Environment(cr, SUPERUSER_ID, {})
            importer = env['google.sheets.integration']
            importer.import_to_sale_order()

if __name__ == "__main__":
    main()
