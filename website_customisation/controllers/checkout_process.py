# # -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request
from odoo import fields, http, SUPERUSER_ID, tools, _
from werkzeug.exceptions import Forbidden, NotFound


class RequestQuotation(http.Controller):
    # @http.route(['/shop/request_quotation'], type='http', auth="public", method=['POST'], website=True)
    # def request_quotation(self):
    #     return request.render('website_customisation.request_for_quotation')

    @http.route('/shop/request_quotation/sent<string:variable>', type='http', auth="public", website=True, sitemap=False)
    def quotation_sent(self, **kwargs):
        values = dict(kwargs)
        return request.render('website_customisation.quotation_confirmation', values)

    @http.route('/shop/request_quotation/submit', type='http', auth="public", website=True, sitemap=False)
    def quotation_submit(self, sale_order_id=None, **post):
        if sale_order_id is None:
            order = request.website.sale_get_order()
        else:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            assert order.id == request.session.get('sale_last_order_id')

        if order:
            request.session['sale_order_id'] = None

        values = {
            'order_name': order.name
        }
        request.website.sale_reset()

        if order.state == 'draft':
            order.write({
                'state': 'website'
            })
            return request.redirect("/shop/request_quotation/sent%s" % order.name)
