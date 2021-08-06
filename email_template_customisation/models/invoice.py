from odoo import models, _, fields, api

from odoo.tools.misc import get_lang


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    def action_invoice_sent(self):
        res = super(AccountMoveInherit, self).action_invoice_sent()
        template_id = False
        self.ensure_one()
        if self.state == 'posted':
            template_id = self.env.ref('email_template_customisation.email_template_invoice_send', raise_if_not_found=False)
        lang = False
        if template_id:
            lang = template_id._render_lang(self.ids)[self.id]
        if not lang:
            lang = get_lang(self.env).code
        compose_form = self.env.ref('account.account_invoice_send_wizard_form', raise_if_not_found=False)
        ctx = dict(
            default_model='account.move',
            default_res_id=self.id,
            # For the sake of consistency we need a default_res_model if
            # default_res_id is set. Not renaming default_model as it can
            # create many side-effects.
            default_res_model='account.move',
            default_use_template=bool(template_id),
            default_template_id=template_id and template_id.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            custom_layout="mail.mail_notification_paynow",
            model_description=self.with_context(lang=lang).type_name,
            force_email=True,
            default_lang=self.partner_id.lang,
        )
        return {
            'name': _('Send Invoice'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice.send',
            'static': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
        res['context'] = ctx
        return res
