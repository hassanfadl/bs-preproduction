from odoo import models, fields, api
from odoo.tools.float_utils import float_compare


class StockMoveInherited(models.Model):
    _inherit = 'stock.move'

    is_checked = fields.Boolean("Checked", default=False)


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    x_studio_color = fields.Char("Color", readonly=True)
    x_studio_foc_qty = fields.Char("FOC Qty", readonly=True)


class ProductionLotSN(models.Model):
    _inherit = 'stock.production.lot'

    x_studio_carton_number = fields.Char("Carton Number")
    sale_order_ids = fields.Many2many('sale.order', string="Sales Orders", compute='_compute_sale_order_ids', readonly=True, store=False)
    sale_order_count = fields.Integer('Sales order count', compute='_compute_purchase_order_ids')
    purchase_order_ids = fields.Many2many('purchase.order', string="Purchase Orders",
                                          compute='_compute_purchase_order_ids', readonly=True, store=False)
    purchase_order_count = fields.Integer('Purchase order count', compute='_compute_purchase_order_ids')
    supplier_id = fields.Char('Vendor')
    x_studio_color = fields.Char("Color")
    product_qty = fields.Float('Counted Quantity')
    x_studio_foc_qty = fields.Char("FOC Qty")
    x_studio_depth_d = fields.Float("Depth")
    x_studio_width_w = fields.Float("Width")
    x_studio_cbm = fields.Float("CBM")
    x_studio_height_h = fields.Float("Height")
    x_studio_gross_weight = fields.Float("GW")
    x_studio_net_weight = fields.Float("NW")
    cbm = fields.Float("CBM", compute='compute_cbm', readonly=True)

    @api.model
    def _compute_sale_order_ids(self):
        for lot in self:
            stock_moves = self.env['stock.move.line'].search([
                ('lot_id', '=', lot.id),
                ('state', '=', 'done')
            ]).mapped('move_id')
            stock_moves = stock_moves.search([('id', 'in', stock_moves.ids)]).filtered(
                lambda move: move.picking_id.location_id.usage == 'supplier' and move.state == 'done')
            lot.sale_order_ids = stock_moves.mapped('sale_line_id.order_id')
            lot.sale_order_count = len(lot.sale_order_ids)

    @api.model
    def _compute_purchase_order_ids(self):
        for lot in self:
            stock_moves = self.env['stock.move.line'].search([
                ('lot_id', '=', lot.id),
                ('state', '=', 'done')
            ]).mapped('move_id')
            stock_moves = stock_moves.search([('id', 'in', stock_moves.ids)]).filtered(
                lambda move: move.picking_id.location_id.usage == 'supplier' and move.state == 'done')
            lot.purchase_order_ids = stock_moves.mapped('purchase_line_id.order_id')
            lot.purchase_order_count = len(lot.purchase_order_ids)

    def action_view_po(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_form_action")
        action['domain'] = [('id', 'in', self.mapped('purchase_order_ids.id'))]
        action['context'] = dict(self._context, create=False)
        return action

    def compute_cbm(self):
        for rec in self:
            rec.cbm = rec.x_studio_depth_d * rec.x_studio_width_w * rec.x_studio_height_h / 1000000

