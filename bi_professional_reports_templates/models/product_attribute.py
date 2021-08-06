# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    def check_report_values(self, partner, value):
        attribute_id = self.env['ir.translation'].search([('lang', '=', partner.lang), ('value', '=', self.name), ('src', '=', value)])
        if attribute_id or self.name == value:
            return True
        return False
