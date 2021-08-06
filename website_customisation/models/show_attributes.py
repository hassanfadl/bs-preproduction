# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ShowAttribute(models.Model):
    _inherit = ["product.attribute", "website.published.mixin"]
    _name = "product.attribute"

    show_in_comparison = fields.Boolean(default=True)
    show_in_right_side = fields.Boolean(default=True)
    show_in_specification = fields.Boolean(default=True)
    show_in_attribute_filter = fields.Boolean(default=True)

