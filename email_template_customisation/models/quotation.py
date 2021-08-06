from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    def action_quotation_send(self, force_confirmation_template=False):
        res = super(SaleOrderInherit, self).action_quotation_send()
        template_id = False

        if force_confirmation_template or (self.state == 'sale' and not self.env.context.get('proforma', False)):
            template_id = int(self.env['ir.config_parameter'].sudo().get_param('sale.default_confirmation_template'))
            template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
            if not template_id:
                template_id = self.env['ir.model.data'].xmlid_to_res_id(
                    'email_template_customisation.mail_template_sale_confirmation_inherit',
                    raise_if_not_found=False)
        if self.state == 'draft':
            template_id = self.env['ir.model.data'].xmlid_to_res_id('email_template_customisation.email_template_quotation_send',
                                                                    raise_if_not_found=False)
        elif self.state == 'sale':
            template_id = self.env['ir.model.data'].xmlid_to_res_id(
                'email_template_customisation.mail_template_sale_confirmation_inherit',
                raise_if_not_found=False)
        if not template_id:
            template_id = self.env['ir.model.data'].xmlid_to_res_id('email_template_customisation.email_template_quotation_send',
                                                                    raise_if_not_found=False)
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang).type_name,
            'default_lang': self.partner_id.lang,
        }
        res['context'] = ctx
        return res
