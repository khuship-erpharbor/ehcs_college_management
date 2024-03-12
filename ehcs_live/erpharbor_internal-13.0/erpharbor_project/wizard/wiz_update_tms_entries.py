# -*- coding: utf-8 -*-
from odoo import api, models


class WizUpdateTMSEntries(models.TransientModel):
    _name = 'wiz.update.tms.entries'

    def update_tms_entries(self):
        lines = self.env['account.analytic.line'].browse(self.env.context.get('active_ids', []))
        lines.write({'is_invoiced': True})
        return True
