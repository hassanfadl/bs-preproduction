from odoo import api, fields, models
from odoo.tools.float_utils import float_compare


class StockImmediateTransferLine(models.TransientModel):
    _inherit = 'stock.backorder.confirmation.line'
    _description = 'Backorder Confirmation Lines'

    backorder_confirmation_id = fields.Many2one('stock.backorder.confirmation', 'Backorder Confirmation', required=True)
    picking_id = fields.Many2one('stock.picking', 'Transfer')
    product_id = fields.Many2one('product.product', string='Product')
    to_process_backorder = fields.Boolean('To Process')
    to_backorder = fields.Boolean('To Process')


class StockBackorderConfirmation(models.TransientModel):
    _inherit = 'stock.backorder.confirmation'
    _description = 'Backorder Confirmation'

    pick_ids = fields.Many2many('stock.picking', 'stock_picking_backorder_rel')
    product_id = fields.Many2one('product.product', string='Product')
    show_transfers = fields.Boolean()
    backorder_confirmation_line_id = fields.One2many(
        'stock.backorder.confirmation.line',
        'backorder_confirmation_id',
        string="Backorder Confirmation Lines")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if 'backorder_confirmation_line_id' in fields and res.get('pick_ids'):
            vals_array = []
            for pick_id in res['pick_ids'][0][2]:
                stock_picking = self.env['stock.picking'].browse(pick_id)
                for line in stock_picking.move_ids_without_package:
                    vals = (0, 0,
                            {'to_process_backorder': True,
                             'picking_id': pick_id,
                             'product_id': line.product_id.id,
                             })
                    vals_array.append(vals)
            res['backorder_confirmation_line_id'] = vals_array
        return res

    def create_selected_backorder(self):
        confirmation_line = self.backorder_confirmation_line_id.filtered(lambda l:l.to_process_backorder)
        products = confirmation_line.mapped('product_id')
        moves_list = []
        for product in products:
            for prd in confirmation_line:
                print(prd.product_id,"prd")
                print(product,"product")
            product_line = confirmation_line.filtered(lambda l : l.product_id.id == product.id)
            pick_id = product_line.mapped('picking_id')
            move_id = self.env['stock.move'].search([('picking_id','=',pick_id[0].id),('product_id','=',product.id)])
            # .filtered(lambda l:l.product_uom_qty != l.quantity_done)
            if move_id:
                moves_list.extend(move_id.filtered(lambda mid: mid.state not in ['cancel', 'done']).ids)
            demand = 0
            done = 0
            for move in move_id:

                demand += move.product_uom_qty
                done += move.quantity_done
                move._action_done(True)
            pick_id.move_ids_without_package.filtered(lambda mid: mid.state == 'cancel' and mid.quantity_done == 0).unlink()
            Stock_move = self.env['stock.move']
            vals = {
                'product_id': product.id,
                'name': product.name,
                'origin': move_id[0].origin,
                'location_id': move_id[0].location_id.id,
                'location_dest_id': move_id[0].location_dest_id.id,
                'product_uom': move_id[0].product_uom.id,
                'product_uom_qty': demand - done,
                'price_unit': move_id[0].price_unit,
                'picking_id': pick_id[0].id,
                'color_id': move_id[0].color_id and move_id[0].color_id.id,
                'move_dest_ids': move_id[0].move_dest_ids and [(6, 0, move_id[0].move_dest_ids.ids)]
            }
            new_mo = Stock_move.create(vals)
            new_mo._action_confirm()

        pick_backorder_id = product_line.mapped('picking_id')
        pick_backorder_id.write({'last_backorder_move_ids': [(6, 0, moves_list)]})
        return True

    def process_cancel_backorder(self):
        pickings_to_validate = self.env.context.get('button_validate_picking_ids')
        if pickings_to_validate:
            return self.env['stock.picking'] \
                .browse(pickings_to_validate) \
                .with_context(skip_backorder=True, picking_ids_not_to_backorder=self.pick_ids.ids) \
                .button_validate()
        return True
