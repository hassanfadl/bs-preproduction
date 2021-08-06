from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    color_id = fields.Many2one('product.color', readonly = False)

    def _prepare_procurement_values(self):
        res = super(StockMove, self)._prepare_procurement_values()
        if self.color_id:
            res['color_id'] = self.color_id.id
        return res