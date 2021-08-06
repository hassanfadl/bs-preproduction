from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ToleranceRate(models.Model):
    _inherit = 'res.partner'

    tolerance_rate = fields.Float(string="Tolerance %")


class OrderlineTolerence(models.Model):
    _inherit = 'sale.order.line'

    # tolerance_rate = fields.Float(string="Tolerence %", related="order_partner_id.tolerance_rate", readonly=False)
    partner_id = fields.Many2one(string="Customer", related='order_id.partner_id', readonly=True)
    # tolerance_rate = fields.Float(string="Tolerence %", default=lambda self: self.partner_id.tolerance_rate,readonly=False)
    tolerance_rate = fields.Float(string="Tolerence %",compute="get_tolerance",store=True, readonly=False)

    @api.depends('partner_id')
    @api.onchange('partner_id')
    def get_tolerance(self):
        for rec in self:
            rec.tolerance_rate = rec.partner_id.tolerance_rate


class POOrderlineTolerence(models.Model):
    _inherit = 'purchase.order.line'

    tolerance_rate = fields.Float(string="Tolerence %", compute="get_tolerance_value", readonly=False)

    def get_tolerance_value(self):
        for record in self:
            channels = self.env['sale.order'].search([('name', '=', record.order_id.origin)])
            if len(channels.order_line.ids) > 0 and channels.order_line.filtered(lambda x: x.product_id and x.product_id.id == record.product_id.id):
                sale_order_line = channels.order_line.filtered(lambda x: x.product_id.id == record.product_id.id)
                record.tolerance_rate = sale_order_line[0].tolerance_rate


class StockOrderlineTolerence(models.Model):
    _inherit = 'stock.move'

    tolerance_rate = fields.Float(string="Tolerence %", compute="get_tolerance_value")

    def get_tolerance_value(self):
        for record in self:
            for rec in record:
                channels = self.env['purchase.order'].search([('name', '=', record.origin)])
                if not channels:
                    channels = self.env['sale.order'].search([('name', '=', record.origin)])
                if len(channels.order_line.ids) > 0:
                    rec.tolerance_rate = channels.order_line[0].tolerance_rate
                else:
                    rec.tolerance_rate = 0
                    if rec.sale_line_id:
                        rec.tolerance_rate = rec.sale_line_id.tolerance_rate
                    elif rec.purchase_line_id:
                        rec.tolerance_rate = rec.purchase_line_id.tolerance_rate


class POrderInherit(models.Model):
    _inherit = 'purchase.order'

    tolerance_check = fields.Boolean("Tolerance Check")
    # total_tax = fields.Monetary(string='Tax %', store=True, readonly=True, compute='_total_tax')
    #
    # @api.depends('order_line.price_subtotal')
    # def _total_tax(self):
    #     for order in self:
    #         amount_untaxed = total_tax = 0.0
    #         for line in order.order_line:
    #             # line._compute_amount()
    #             individual_tax = (line.price_subtotal * line.vendor_tax) / 100
    #             amount_untaxed += line.price_subtotal
    #             total_tax += line.individual_tax
    #         order.update({
    #             'amount_untaxed': order.currency_id.round(amount_untaxed),
    #             'total_tax': total_tax,
    #             'amount_total': amount_untaxed + total_tax,
    #         })
