# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class MailTemplateInherited(models.Model):
    _inherit = 'mail.template'

    active = fields.Boolean('Active', default=True)
