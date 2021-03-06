# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models, _
# import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError, RedirectWarning, ValidationError, Warning
from operator import itemgetter
from odoo.tools import groupby
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class StockPicking(models.Model):
    _inherit = "stock.picking"

    # invisible = fields.Char(string="Invisible")
    sale_ids = fields.Many2many('sale.order', string='sale references')
    purchase_ids = fields.Many2many('purchase.order', string='Purchase references')
    x_studio_order_reference = fields.Char('Sale Order', compute='get_values', readonly=True)
    x_studio_customer_reference_ = fields.Char('Customer Name', compute='get_data', readonly=True)
    x_studio_so = fields.Char('Related Order (PO/SO)', compute='compute_related_po_so')
    last_backorder_move_ids = fields.Many2many('stock.move', string='Last Backorders')

    def get_values(self):
        for record in self:
            channels = self.env['purchase.order'].search([('name', '=', record.origin)])
            ref = channels.origin
            record.x_studio_order_reference = ref

    def get_data(self):
        for record in self:
            # channels = self.env['sale.order'].search([('name', '=', record.x_studio_order_reference)])
            # cust = channels.partner_id
            # self.x_studio_customer_reference_ = cust.name
            if record.sale_ids:
                client_order_ref = ''
                for rec in record.sale_ids:
                    if rec.origin:
                        if client_order_ref:
                            client_order_ref += ', '
                        client_order_ref = rec.origin
                    elif rec.client_order_ref:
                        if client_order_ref:
                            client_order_ref += ', '
                        client_order_ref += rec.client_order_ref
                record.x_studio_customer_reference_ = client_order_ref
            else:
                channel = self.env['sale.order'].search([('name', '=', record.x_studio_order_reference)], limit=1)
                if not channel:
                    channel = self.env['sale.order'].search([('name', '=', record.origin)], limit=1)
                record.x_studio_customer_reference_ = channel.client_order_ref

    def compute_related_po_so(self):
        for record in self:
            channel = self.env['purchase.order'].search([('origin', '=', record.origin)], limit=1)
            record.x_studio_so = channel.name

    def button_validate(self):
        validate_picking = {}
        for record in self:
            move_id = self.env['stock.move'].search([('picking_id', '=', record.id)])
            if move_id:
                validate_picking.update({record.id: move_id.filtered(lambda mid: mid.state not in ['cancel', 'done']).ids})
                # moves_list.extend(move_id.filtered(lambda mid: mid.state not in ['cancel', 'done']).ids)
            if record.picking_type_id.code == 'incoming' and record.move_ids_without_package.mapped('move_dest_ids'):
                moves = groupby(record.move_ids_without_package, itemgetter('move_dest_ids'))
                for move in moves:
                    managed_qty = move[0].product_uom_qty * move[0].tolerance_rate / 100
                    total_done_qty = 0
                    for po_move in move[1]:
                        total_done_qty += po_move.quantity_done
                    if total_done_qty >= move[0].product_uom_qty + managed_qty:
                        move[0].write({'product_uom_qty': move[0].product_uom_qty + managed_qty})
        res = super(StockPicking, self).button_validate()
        if isinstance(res, bool) and validate_picking:
            for record in self:
                if record.id in validate_picking:
                    record.write({'last_backorder_move_ids': [(6, 0, validate_picking[record.id])]})
        return res

    def button_validate_new(self):

        # Clean-up the context key at validation to avoid forcing the creation of immediate
        # transfers.
        ctx = dict(self.env.context)
        ctx.pop('default_immediate_transfer', None)
        self = self.with_context(ctx)

        # Sanity checks.
        pickings_without_moves = self.browse()
        pickings_without_quantities = self.browse()
        pickings_without_lots = self.browse()
        products_without_lots = self.env['product.product']
        tolerance_value = self.move_ids_without_package
        done_qty = self.move_ids_without_package
        for rec in done_qty:
            # (rec.product_uom_qty * rec.tolerance_rate) / 100
            tolerence_qty = 0.0
            if rec.tolerance_rate:
                tolerence_qty = (rec.product_uom_qty * rec.tolerance_rate) / 100
            if (rec.product_uom_qty + tolerence_qty) >= rec.quantity_done >= (rec.product_uom_qty - tolerence_qty):
                return super(StockPicking, self).with_context(skip_backorder=True, picking_ids_not_to_backorder=self.ids).button_validate()
            if tolerence_qty and rec.quantity_done < (rec.product_uom_qty - tolerence_qty):
                tolerance_value = True
                return {'type': 'ir.actions.act_window',
                        'name': _('Tolerance Checking'),
                        'res_model': 'tolerence.wizard',
                        'target': 'new',
                        'view_mode': 'form',
                        'context': {'tolerance_value': tolerance_value}
                        }
            elif tolerence_qty and rec.quantity_done > (rec.product_uom_qty + tolerence_qty):
                tolerance_value = False
                return {'type': 'ir.actions.act_window',
                        'name': _('Tolerance Checking'),
                        'res_model': 'tolerence.wizard',
                        'target': 'new',
                        'view_mode': 'form',
                        'context': {'tolerance_value': tolerance_value}
                        }
        for picking in self:
            if not picking.move_lines and not picking.move_line_ids:
                pickings_without_moves |= picking

            picking.message_subscribe([self.env.user.partner_id.id])
            picking_type = picking.picking_type_id
            precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            no_quantities_done = all(
                float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in
                picking.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
            no_reserved_quantities = all(
                float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line
                in picking.move_line_ids)
            if no_reserved_quantities and no_quantities_done:
                pickings_without_quantities |= picking
            if picking_type.use_create_lots or picking_type.use_existing_lots:
                lines_to_check = picking.move_line_ids
                if not no_quantities_done:
                    lines_to_check = lines_to_check.filtered(
                        lambda line: float_compare(line.qty_done, 0, precision_rounding=line.product_uom_id.rounding))
                for line in lines_to_check:
                    product = line.product_id
                    if product and product.tracking != 'none':
                        if not line.lot_name and not line.lot_id:
                            pickings_without_lots |= picking
                            products_without_lots |= product

        if not self._should_show_transfers():
            if pickings_without_moves:
                raise UserError(_('Please add some items to move.'))
            if pickings_without_quantities:
                raise UserError(self._get_without_quantities_error_message())
            if pickings_without_lots:
                raise UserError(_('You need to supply a Lot/Serial number for products %s.') % ', '.join(
                    products_without_lots.mapped('display_name')))
        else:
            message = ""
            if pickings_without_moves:
                message += _('Transfers %s: Please add some items to move.') % ', '.join(
                    pickings_without_moves.mapped('name'))
            if pickings_without_quantities:
                message += _(
                    '\n\nTransfers %s: You cannot validate these transfers if no quantities are reserved nor done. To force these transfers, switch in edit more and encode the done quantities.') % ', '.join(
                    pickings_without_quantities.mapped('name'))
            if pickings_without_lots:
                message += _('\n\nTransfers %s: You need to supply a Lot/Serial number for products %s.') % (
                    ', '.join(pickings_without_lots.mapped('name')),
                    ', '.join(products_without_lots.mapped('display_name')))
            if message:
                raise UserError(message.lstrip())

        # Run the pre-validation wizards. Processing a pre-validation wizard should work on the
        # moves and/or the context and never call `_action_done`.
        if not self.env.context.get('button_validate_picking_ids'):
            self = self.with_context(button_validate_picking_ids=self.ids)
        res = self._pre_action_done_hook()
        if res is not True:
            return res

        # Call `_action_done`.

        if self.env.context.get('picking_ids_not_to_backorder'):
            pickings_not_to_backorder = self.browse(self.env.context['picking_ids_not_to_backorder'])
            pickings_to_backorder = self - pickings_not_to_backorder
        else:
            pickings_not_to_backorder = self.env['stock.picking']
            pickings_to_backorder = self
        pickings_not_to_backorder.with_context(cancel_backorder=True)._action_done()
        pickings_to_backorder.with_context(cancel_backorder=False)._action_done()
        return True
