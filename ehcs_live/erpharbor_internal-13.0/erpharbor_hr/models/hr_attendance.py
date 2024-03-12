# coding: utf-8
from datetime import datetime

from odoo import fields, models


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    def action_check_entry(self):
        today = datetime.today()
        email_template = self.env.ref('erpharbor_hr.hr_attendance_template')
        for attandance in self.env['hr.attendance'].search([('check_out','=',False)]):
            attandance.check_out = today
            if email_template:
                email_template.send_mail(attandance.id, force_send=True)
