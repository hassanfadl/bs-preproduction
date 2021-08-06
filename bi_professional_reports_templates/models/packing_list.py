from odoo import models, api, fields


class StockProductionLotInherit(models.Model):
    _inherit = 'stock.production.lot'

    product_qty = fields.Float('Quantity', compute='_product_qty', store=True)


class PackingListReportPrint(models.Model):
    _name = 'report.packing_list.print_packing_list_report'

    @api.model
    def _get_report_values(self, docids, data):
        docs = self.env['stock.picking'].browse(docids)
        return {
            'docs': docs,
        }

