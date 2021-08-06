from odoo import models, fields, api


class SaleOrderRecoveryInherit(models.Model):
    _inherit = "sale.order"

    def action_recovery_email_send(self):
        res = super(SaleOrderRecoveryInherit, self).action_recovery_email_send()
        template_ids = False
        if self.state == 'draft':
            template_ids = self.env['ir.model.data'].xmlid_to_res_id('email_template_customisation.mail_template_revised_quotation_inherit',
                                                                    raise_if_not_found=False)
            print("template_ids",template_ids)
        self.ensure_one()
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_ids)
        template.send_mail(self.id, force_send=True)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_composition_mode': 'mass_mail' if len(self.ids) > 1 else 'comment',
            'default_res_id': self.ids[0],
            'default_model': 'sale.order',
            'default_use_template': bool(template_ids),
            'default_template_id': template_ids,
            'website_sale_send_recovery_email': True,
            'active_ids': self.ids,
            'default_lang': self.partner_id.lang,
        }
        res['context'] = ctx
        return res

