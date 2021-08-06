from odoo import models, fields, api


class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"

    def action_rfq_send(self):
        '''
        This function opens a window to compose an email, with the edi purchase template message loaded by default
        '''
        self.ensure_one()
        template_id = False
        res = super(PurchaseOrderInherit, self).action_rfq_send()
        ir_model_data = self.env['ir.model.data']
        template_id = ir_model_data.get_object_reference('email_template_customisation',
                                                             'email_template_purchase_done')[1]
        ''' To set Purchase Order: Send PO email template as default '''
        # if self.state == 'purchase':
        # elif self.state == 'draft':
        #     template_id = ir_model_data.get_object_reference('email_template_customisation',
        #                                                      'email_template_purchase_confirm')[
        #         1]
        # elif self.state == 'sent':
        #     template_id = ir_model_data.get_object_reference('purchase',
        #                                                      'email_template_edi_purchase_done')[
        #         1]
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        # for record in self:
        #     customer = self.env['sale.order'].search([('name', '=', record.origin)])
        ctx = {
            'default_model': 'purchase.order',
            'active_model': 'purchase.order',
            'active_id': self.ids[0],
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            'mark_rfq_as_sent': True,
            'default_lang': self.partner_id.lang,
            'lang': self.partner_id.lang,
        }
        res['context'] = ctx
        return res
