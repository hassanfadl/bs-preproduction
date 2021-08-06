from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    color_ids = fields.Many2many('product.color', string = 'Colors')