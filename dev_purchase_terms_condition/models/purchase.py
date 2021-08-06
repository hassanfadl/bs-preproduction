# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import fields, models, api


class Purchase(models.Model):
    _inherit = 'purchase.order'

    terms_id = fields.Many2one('purchase.term.condition', string='Terms & Conditions')

    @api.onchange('terms_id')
    def onchange_term_condition(self):
        if self.terms_id:
            self.notes = self.terms_id.with_context({'lang': self.partner_id.lang}).terms

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: