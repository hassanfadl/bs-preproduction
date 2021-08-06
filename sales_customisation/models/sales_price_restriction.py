# -*- coding: utf-8 -*-

from odoo import models, fields, _, api

S = "qwqw"


class SalesPriceRestriction(models.Model):
    _inherit = 'sale.order'

    # state = fields.Selection([('new state', 'To Approve')])
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('to approve', 'To approve'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    previous_state = fields.Char(string='Previous State')

    @api.onchange('price_unit')
    def action_click(self):
        products = []
        user_group = self.env.ref('purchase.group_purchase_user')
        self.env.user.groups_id += user_group
        for line in self.order_line:
            product_details = line.product_id._get_combination_info_variant(add_qty = line.product_uom_qty,
                                                                            pricelist = self.pricelist_id)
            if product_details.get('price', False):
                pricelist_price = product_details.get('price')
            else:
                pricelist_price = line.product_id.lst_price
            price_unit = line.price_unit
            approved_price = line.approved_price
            if approved_price:
                pricelist_price = approved_price
            if price_unit < pricelist_price:
                self.write({'previous_state': 'draft',
                            'state': 'to approve'})
                products.append(line.product_id)
        if len(products) == 0:
            self.write({'previous_state': 'draft',
                        'state': 'sent'})
        groups_ids = self.env.user.groups_id.filtered(lambda p: p.id != user_group.id)
        self.env.user.groups_id = groups_ids

    def action_confirm(self):
        products = []
        for line in self.order_line:
            product_details = line.product_id._get_combination_info_variant(add_qty = line.product_uom_qty,
                                                                            pricelist = self.pricelist_id)
            if product_details.get('price', False):
                pricelist_price = product_details.get('price')
            else:
                pricelist_price = line.product_id.lst_price
            price_unit = line.price_unit
            approved_price = line.approved_price
            if approved_price:
                pricelist_price = approved_price
            if price_unit < pricelist_price:
                self.write({'previous_state': 'sent',
                            'state': 'to approve'})
                products.append(line.product_id)
        if len(products) == 0:
            return super(SalesPriceRestriction, self).action_confirm()
        return True

    def button_approve(self, force=False):
        for line in self.order_line:
            line.approved_price = line.price_unit
        self.write({'state': self.previous_state})
        return {}

    def button_disapprove(self, force=False):
        self.write({'state': self.previous_state})
        return {}


class SalesOrderLine(models.Model):
    _inherit = 'sale.order.line'

    approved_price = fields.Monetary('Approved Price', readonly = True)
    color_id = fields.Many2one('product.color')

    def _prepare_invoice_line(self, **optional_values):
        res = super(SalesOrderLine, self)._prepare_invoice_line(**optional_values)
        res.update({'color_id': self.color_id.id})
        return res

    def _prepare_procurement_values(self, group_id=False):
        res = super(SalesOrderLine, self)._prepare_procurement_values(group_id)
        res['color_id'] = self.color_id.id
        return res

    def _compute_tax_id(self):
        for line in self:
            line = line.with_company(line.company_id)
            fpos = line.order_id.fiscal_position_id or line.order_id.fiscal_position_id.get_fiscal_position(line.order_partner_id.id)
            # If company_id is set, always filter taxes by the company
            taxes = line.product_id.taxes_id.filtered(lambda t: t.company_id == line.env.company)
            if not taxes:
                taxes = line.company_id.account_sale_tax_id
            line.tax_id = fpos.map_tax(taxes, line.product_id, line.order_id.partner_shipping_id)






