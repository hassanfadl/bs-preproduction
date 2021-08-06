from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    color_id = fields.Many2one('product.color')