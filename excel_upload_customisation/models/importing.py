import binascii
import tempfile
import xlrd
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError, RedirectWarning

from odoo import models, fields, _, api


class ImportLots(models.TransientModel):
    _name = 'production.lot.wizard'

    file_name = fields.Binary()

    def action_import_lots(self):
        fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.file_name))
        fp.seek(0)
        stock_move_line = self.env['stock.move.line']
        lot_obj = self.env['stock.production.lot']
        ir_sequence_obj = self.env['ir.sequence']
        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)
        rows = [sheet.row_values(i) for i in range(10, sheet.nrows) if sheet.row_values(i)[0] != '']
        po_no = [row[1] for row in rows]
        purchase_order = self.env['purchase.order'].search([('name', 'in', po_no)])
        move_ids = purchase_order.picking_ids.mapped('move_ids_without_package').filtered(lambda x: x.state not in ['done', 'cancel'])
        for row in rows:
            moves = move_ids.filtered(lambda mid: mid.origin and mid.product_id.name == row[3])
            row_count = 0
            for move in moves:
                if (not move.color_id and row[4]) or (move.color_id and move.color_id.name != row[4]):
                    raise UserError('On row: %s, Purchase Order Number: %s, Product Name: %s color value is mismatched!' % (row_count+1, row[1], row[3]))
                if move.is_checked or row_count != 0:
                    continue
                else:
                    row_count += 1
                    move.is_checked = True
                location_dest = move.location_dest_id._get_putaway_strategy(move.product_id) or move.location_dest_id
                lot = ir_sequence_obj.next_by_code('stock.lot.serial')
                lot_id = lot_obj.create({
                    'x_studio_carton_number': row[0],
                    'name': lot,
                    'ref': row[3],
                    'product_id': move.product_id.id,
                    'company_id': self.env.company.id,
                    'x_studio_color': row[4],
                    'x_studio_foc_qty': row[8],
                    'x_studio_height_h': row[11],
                    'x_studio_width_w': row[10],
                    'x_studio_depth_d': row[9],
                    'x_studio_cbm': row[11],
                    'x_studio_gross_weight': row[12],
                    'x_studio_net_weight': row[13],
                })
                move_line = stock_move_line.create({
                    'lot_name': lot_id.name,
                    'qty_done': row[5],
                    'x_studio_color': row[4],
                    'x_studio_foc_qty': row[8],
                    'product_id': move.product_id.id,
                    'product_uom_id': move.product_id.uom_id.id,
                    'location_id': move.location_id.id,
                    'location_dest_id': location_dest.id,
                    'picking_id': move.picking_id.id,
                    'move_id': move.id,
                    'lot_id': lot_id.id
                })
                move.write({
                    'move_line_ids': [(4, move_line.id)],
                })
        move_ids.write({'is_checked': False})
        purchase_order.mapped("picking_ids").button_validate()

    def confirmation_msg(self):
        fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.file_name))
        fp.seek(0)
        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)
        rows = [sheet.row_values(i) for i in range(10, sheet.nrows) if sheet.row_values(i)[0] != '']
        po_no = [sheet.row_values(i)[2] for i in range(10, sheet.nrows) if sheet.row_values(i)[0] != '']
        purchase_order = self.env['purchase.order'].search([('name', 'in', po_no)])
        move_ids = purchase_order.picking_ids.mapped('move_ids_without_package')
        for move in move_ids:
            move_rows = list(filter(lambda row: row[1] == move.origin and move.product_id.name == row[3], rows))
            if len(move_rows) > 0 and move.quantity_done > 0:
                return {
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'view_id': self.env.ref('excel_upload_customisation.condition_checking_wizard').id,
                    'res_model': 'production.lot.wizard',
                    'res_id': self.id,
                    'target': 'new'
                }

        self.action_import_lots()
        message = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success!'),
                'message': 'Importing Completed Successfully',
                'sticky': False,
            }
        }
        return message
