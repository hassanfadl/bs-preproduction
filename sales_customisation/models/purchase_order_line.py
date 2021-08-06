from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    color_id = fields.Many2one('product.color')


    def _prepare_purchase_order_line_from_procurement(self, product_id, product_qty, product_uom, company_id, values, po):
        res = super(PurchaseOrderLine, self)._prepare_purchase_order_line_from_procurement(product_id, product_qty, product_uom, company_id, values, po)
        if values.get('color_id'):
            res['color_id'] = values.get('color_id')
        order_id = self.env['purchase.order'].browse(res.get('order_id'))
        taxes = product_id.supplier_taxes_id
        if not taxes:
            taxes = order_id.company_id.account_purchase_tax_id
        fpos = po.fiscal_position_id
        partner  = values.get('supplier')
        seller = product_id.with_company(company_id)._select_seller(
            partner_id = partner.name,
            quantity = product_qty,
            date = po.date_order and po.date_order.date(),
            uom_id = product_id.uom_po_id)
        taxes_id = fpos.map_tax(taxes, product_id, seller.name)
        if taxes_id:
            taxes_id = taxes_id.filtered(lambda x: x.company_id.id == company_id.id)
        res['taxes_id'] = [(6, 0, taxes_id.ids)]
        return res

    def _prepare_account_move_line(self, move=False):
        res = super(PurchaseOrderLine, self)._prepare_account_move_line()
        if self.color_id:
            res['color_id'] = self.color_id.id
        return res

    def _prepare_stock_move_vals(self, picking, price_unit, product_uom_qty, product_uom):
        res = super(PurchaseOrderLine, self)._prepare_stock_move_vals(picking, price_unit, product_uom_qty, product_uom)
        if self.color_id:
            res['color_id'] = self.color_id.id
        return res

    def _compute_tax_id(self):
        for line in self:
            line = line.with_company(line.company_id)
            fpos = line.order_id.fiscal_position_id or line.order_id.fiscal_position_id.get_fiscal_position(line.order_id.partner_id.id)
            # filter taxes by company
            taxes = line.product_id.supplier_taxes_id.filtered(lambda r: r.company_id == line.env.company)
            if not taxes:
                taxes = line.company_id.account_purchase_tax_id
            line.taxes_id = fpos.map_tax(taxes, line.product_id, line.order_id.partner_id)

