# -*- coding: utf-8 -*-

from odoo.http import request
import json
from odoo import http, SUPERUSER_ID
# from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSale(http.Controller):

    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        """This route is called when adding a product to cart (no options)."""
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.is_draft:
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)

        product_custom_attribute_values = None
        if kw.get('product_custom_attribute_values'):
            product_custom_attribute_values = json.loads(kw.get('product_custom_attribute_values'))

        no_variant_attribute_values = None
        if kw.get('no_variant_attribute_values'):
            no_variant_attribute_values = json.loads(kw.get('no_variant_attribute_values'))

        sale_order._cart_update(
            product_id=int(product_id),
            set_qty=set_qty,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values
        )
        return request.redirect("/shop")

