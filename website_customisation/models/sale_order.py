# -*- coding: utf-8 -*-

from odoo import models


class SaleOrderInherited(models.Model):
    _inherit = 'sale.order'

    def has_to_be_signed(self, include_draft=False):
        res = super(SaleOrderInherited, self).has_to_be_signed(include_draft=include_draft)
        if res:
            lower_value = False
            for line in self.order_line:
                product_details = line.product_id._get_combination_info_variant(add_qty = line.product_uom_qty,
                                                                                pricelist = self.pricelist_id)
                if product_details.get('price', False):
                    pricelist_price = product_details.get('price')
                else:
                    pricelist_price = line.product_id.lst_price
                price_unit = line.price_unit
                approved_price = line.approved_price
                if approved_price:
                    pricelist_price = approved_price
                if price_unit < pricelist_price:
                    lower_value = True
                    break
            if lower_value:
                return False
        return res
