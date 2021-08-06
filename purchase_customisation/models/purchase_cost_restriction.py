# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseCostRestriction(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
        ('draft', 'SO Received'),
        ('to approve', 'To Approve'),
        ('sent', 'PO Sent'),
        ('sent approval', 'Approval waiting'),
        ('purchase', 'PO Confirmed'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    name = fields.Char('SO Number', required=True, index=True, copy=False, default='New')
    previous_state = fields.Char('Previous State')
    grey_cloth = fields.Char('1.坯布')
    swatches = fields.Char('2.色板')
    test = fields.Char('3.測試')
    quality_board = fields.Char('4.大貨質量板')
    pallets = fields.Char('5.大貨板')
    finished_products = fields.Char('6.成品')
    quality_inspection = fields.Char('7.品檢')
    logistic_delivery = fields.Char('8.物流送貨')
    remarks = fields.Char('9.備註')
    packing_requirements = fields.Char('10.包裝/裝箱要求')

    def action_click(self):
        for order in self:
            order_line = order.order_line
            products = []
            for line in order_line:
                price_unit = line.get_unit_price()
                if price_unit:
                    pricelist_price = price_unit
                else:
                    pricelist_price = line.product_id.standard_price
                approved_price = line.approved_price
                if approved_price:
                    pricelist_price = approved_price
                if line.price_unit > pricelist_price:
                    order.write({'state': 'sent approval',
                                'previous_state': 'draft'})
                    products.append(line.product_id)
            if len(products) == 0:
                order.write({'state': 'sent'})
        return True

    def button_confirm(self):
        for order in self:
            order_line = order.order_line
            products = []
            for line in order_line:
                price_unit = line.get_unit_price()
                if price_unit:
                    pricelist_price = price_unit
                else:
                    pricelist_price = line.product_id.standard_price
                approved_price = line.approved_price
                if approved_price:
                    pricelist_price = approved_price
                if line.price_unit > pricelist_price:
                    order.write({'state': 'sent approval',
                                'previous_state': order.state})
                    products.append(line.product_id)
            if len(products) == 0:
                order.write({'state': 'sent'})
                super(PurchaseCostRestriction, order).button_confirm()
        return True

    def action_approve(self, force=False):
        for line in self.order_line:
            line.approved_price = line.price_unit
        self.write({'state': self.previous_state or 'draft'})
        return {}

    def button_disapprove(self, force=False):
        self.write({'state': self.previous_state or 'draft',
                    'previous_state': self.previous_state or 'draft'})
        return {}

    def name_get(self):
        result = []
        for record in self:
            name = 'Purchase Preparation'
            result.append((record.id, name))
        return result
