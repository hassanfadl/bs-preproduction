# -*- coding: utf-8 -*-

from odoo import models


class ExcelToleranceWizard(models.TransientModel):
    _name = "excel.tolerance.wizard"
    _description = "Excel Tolerance Wizard"

    def continue_validate(self):
        if 'excel_upload' in self.env.context:
            lot_wizard_id = self.env['production.lot.wizard'].browse(self.env.context['excel_upload'])
            return lot_wizard_id.with_context({'confirm_excel': True}).confirmation_msg()
        return True
