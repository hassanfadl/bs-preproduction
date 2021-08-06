from odoo import models, fields, api


class ResPartnerInherited(models.Model):
    _inherit = 'res.partner'

    accessible_user_id = fields.Many2one('res.users', string='Access User')
