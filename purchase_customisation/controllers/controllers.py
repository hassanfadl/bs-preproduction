# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseCustomisation(http.Controller):
#     @http.route('/purchase_customisation/purchase_customisation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_customisation/purchase_customisation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_customisation.listing', {
#             'root': '/purchase_customisation/purchase_customisation',
#             'objects': http.request.env['purchase_customisation.purchase_customisation'].search([]),
#         })

#     @http.route('/purchase_customisation/purchase_customisation/objects/<model("purchase_customisation.purchase_customisation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_customisation.object', {
#             'object': obj
#         })
