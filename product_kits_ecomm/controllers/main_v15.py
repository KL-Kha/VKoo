# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.
# import json
# import logging
# from werkzeug.exceptions import Forbidden, NotFound
# from werkzeug.urls import url_decode, url_encode, url_parse

# from odoo import fields, http, SUPERUSER_ID, tools, _
# from odoo.fields import Command
# from odoo.http import request
# from odoo.addons.base.models.ir_qweb_fields import nl2br
# from odoo.addons.http_routing.models.ir_http import slug
# from odoo.addons.payment.controllers import portal as payment_portal
# from odoo.addons.payment.controllers.post_processing import PaymentPostProcessing
# from odoo.addons.website.controllers.main import QueryURL
# from odoo.addons.website.models.ir_http import sitemap_qs2dom
# from odoo.exceptions import AccessError, MissingError, ValidationError
# from odoo.addons.portal.controllers.portal import _build_url_w_params
# from odoo.addons.website.controllers import main
# from odoo.addons.website.controllers.form import WebsiteForm
# from odoo.osv import expression
# from odoo.tools.json import scriptsafe as json_scriptsafe
# from odoo.addons.website_sale.controllers.main import WebsiteSale
# _logger = logging.getLogger(__name__)


# class CustomWebsiteSale(WebsiteSale):

#     @http.route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
#     def cart_update_json(
#         self, product_id, line_id=None, add_qty=None, set_qty=None, display=True,
#         product_custom_attribute_values=None, no_variant_attribute_values=None, **kw
#     ):
#         """
#         This route is called :
#             - When changing quantity from the cart.
#             - When adding a product from the wishlist.
#             - When adding a product to cart on the same page (without redirection).
#         """
#         order = request.website.sale_get_order(force_create=True)
#         if order.state != 'draft':
#             request.website.sale_reset()
#             if kw.get('force_create'):
#                 order = request.website.sale_get_order(force_create=True)
#             else:
#                 return {}

#         pcav = kw.get('product_custom_attribute_values')
#         nvav = kw.get('no_variant_attribute_values')

#         record_product_template_id = request.env['product.product'].search([('id','=',product_id)])

#         product_kits_check = False
#         if record_product_template_id.product_tmpl_id.x_split_products:
#             product_kits_check = True

#         if product_kits_check == False:
#             value = order._cart_update(
#                 product_id=product_id,
#                 line_id=line_id,
#                 add_qty=add_qty,
#                 set_qty=set_qty,
#                 product_custom_attribute_values=json_scriptsafe.loads(pcav) if pcav else None,
#                 no_variant_attribute_values=json_scriptsafe.loads(nvav) if nvav else None
#             )

#             if not order.cart_quantity:
#                 request.website.sale_reset()
#                 return value

#             order = request.website.sale_get_order()
#             value['cart_quantity'] = order.cart_quantity

#             if not display:
#                 return value

#             value['website_sale.cart_lines'] = request.env['ir.ui.view']._render_template("website_sale.cart_lines", {
#                 'website_sale_order': order,
#                 'date': fields.Date.today(),
#                 'suggested_products': order._cart_accessories()
#             })
#             value['website_sale.short_cart_summary'] = request.env['ir.ui.view']._render_template("website_sale.short_cart_summary", {
#                 'website_sale_order': order,
#             })
#             return value
#         elif product_kits_check == True:
#             for line_kit in record_product_template_id.product_tmpl_id.product_line_kit_ids:
#                 product_id = line_kit.product_kit_template_id.id
#                 add_qty = line_kit.quantity_per_product

#                 value = order._cart_update(
#                     product_id=product_id,
#                     line_id=line_id,
#                     add_qty=add_qty,
#                     set_qty=set_qty,
#                     product_custom_attribute_values=json_scriptsafe.loads(pcav) if pcav else None,
#                     no_variant_attribute_values=json_scriptsafe.loads(nvav) if nvav else None
#                 )

#                 if not order.cart_quantity:
#                     request.website.sale_reset()
#                     return value

#                 order = request.website.sale_get_order()
#                 value['cart_quantity'] = order.cart_quantity

#                 if not display:
#                     return value

#                 value['website_sale.cart_lines'] = request.env['ir.ui.view']._render_template("website_sale.cart_lines", {
#                     'website_sale_order': order,
#                     'date': fields.Date.today(),
#                     'suggested_products': order._cart_accessories()
#                 })
#                 value['website_sale.short_cart_summary'] = request.env['ir.ui.view']._render_template("website_sale.short_cart_summary", {
#                     'website_sale_order': order,
#                 })
#             return value