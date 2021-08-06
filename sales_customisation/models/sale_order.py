from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_abandoned_cart = fields.Boolean('Abandoned Cart', compute='_compute_abandoned_cart', search='_search_abandoned_cart')
    cart_recovery_email_sent = fields.Boolean('Cart recovery email already sent')
    is_draft = fields.Boolean(string="Is Draft")
    state = fields.Selection(selection_add=[('website', 'Website Enquiry'),
                                            ('draft', 'Quotation'),
                                            ('to approve', 'To Approve'),
                                            ('sent', 'Quotation Confirm'),
                                            ('sale', 'Sales Order')])

    x_studio_1_pre_production_sample_ready_1 = fields.Date("1. Pre-production Sample Request")
    x_studio_2_shipment_sample_ready = fields.Date("2. Shipment Sample Ready")
    x_studio_3_finished_goods_ready = fields.Date("3. Finished Goods Ready")

    remarks = fields.Char("Remarks")