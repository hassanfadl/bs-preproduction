# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models


class PurchaseOrderInherited(models.Model):
    _inherit = 'purchase.order'

    def get_bright_sun_company(self):
        ''' This function is used for fetch bright sun company address in odoo_standard_report_purchaseorder_document '''
        bright_sun_company = self.env['res.company'].search([('is_bright_sun', '=', True)], limit=1)
        if not bright_sun_company:
            bright_sun_company = self.env['res.company'].search([], limit=1)
        return bright_sun_company
