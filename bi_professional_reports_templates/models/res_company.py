# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class res_company(models.Model):
    _inherit = "res.company"

    sale_template = fields.Selection([
        ('fency', 'Fency'),
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('odoo_standard', 'Odoo Standard'),
    ], 'Sale')
    purchase_template = fields.Selection([
        ('fency', 'Fency'),
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('odoo_standard', 'Odoo Standard'),
    ], 'Purchase')
    stock_template = fields.Selection([
        ('fency', 'Fency'),
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('odoo_standard', 'Odoo Standard'),
    ], 'Stock')
    account_template = fields.Selection([
        ('fency', 'Fency'),
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('odoo_standard', 'Odoo Standard'),
    ], 'Account')
    ''' To identify bright sun company, It needs to be set only in one company. '''
    is_bright_sun = fields.Boolean('Is Bright Sun', default=False)


class account_invoice(models.Model):
    _inherit = "account.move"

    paypal_chk = fields.Boolean("Paypal")
    paypal_id = fields.Char("Paypal Id")

    def invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        self.ensure_one()
        self.sent = True
        return self.env.ref('bi_professional_reports_templates.custom_account_invoices').report_action(self)


class res_company(models.Model):
    _inherit = "res.company"

    bank_account_id = fields.Many2one('res.partner.bank', 'Bank Account')


class res_partner_bank(models.Model):
    _inherit = "res.partner.bank"

    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', size=24, change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", 'State')
    country_id = fields.Many2one('res.country', 'Country')
    swift_code = fields.Char('Swift Code')
    ifsc = fields.Char('IFSC')
    branch_name = fields.Char('Branch Name')


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    version = fields.Char('Version', readonly=False)

    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        return self.env.ref('bi_professional_reports_templates.custom_report_sale_order').report_action(self)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    x_studio_1_pre_production_sample_ready_1 = fields.Date('1. Pre-production Sample Ready')
    x_studio_2_shipment_sample_ready = fields.Date('2. Shipment Sample Ready')
    x_studio_3_finished_goods_ready = fields.Date('3. Finished Goods Ready')
    # customer_request_date = fields.Char('Customer Request Date', compute='get_values', readonly=True)
    customer_request_date1 = fields.Char('Customer Request Date', compute='get_values', readonly=True)
    version_no = fields.Char('Version', compute='get_version_no', readonly=True)

    def get_version_no(self):
        for record in self:
            ver_no = self.env['sale.order'].search([('name', '=', record.origin)])
            # print("///",ver_no)
            version_num = ver_no.version
            # print("/////", version_num)
            self.version_no = version_num

    def get_values(self):
        for record in self:
            channels = self.env['sale.order'].search([('name', '=', record.origin)])
            req_date = channels.x_studio_3_finished_goods_ready
            self.customer_request_date1 = req_date

    def print_quotation(self):
        self.write({'state': "sent"})
        return self.env.ref('bi_professional_reports_templates.custom_report_purchase_quotation').report_action(self)
