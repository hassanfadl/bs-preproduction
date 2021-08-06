from odoo import models, api


class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    @api.model
    def _get_values(self, docids):
        docs = self.env('stock.picking').browse(docids)
        return {
            'doc_ids': docs.ids,
        }

    def action_delivery_sent(self):
        '''
        This function opens a window to compose an email, with the edi purchase template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        mail_template_id = False
        if self.state == 'done':
            mail_template_id = ir_model_data.get_object_reference('email_template_customisation',
                                                             'email_template_delivery_done')[1]

        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(mail_template_id)
        template.send_mail(self.id, force_send=True)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'stock.picking',
            'active_model': 'stock.picking',
            'active_id': self.ids[0],
            'default_res_id': self.ids[0],
            'default_use_template': bool(mail_template_id),
            'default_template_id': mail_template_id,
            'default_composition_mode': 'comment',
            'force_email': True,
            'default_lang': self.partner_id.lang,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'static': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
