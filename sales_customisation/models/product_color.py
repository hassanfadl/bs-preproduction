from odoo import models, fields


class ProductColor(models.Model):
    _name = 'product.color'
    _description = 'Seperate model to create colors and add it into sale order'
    _rec_name = 'name'

    name = fields.Char('Name', required = True)
    hex_code = fields.Char('Color')