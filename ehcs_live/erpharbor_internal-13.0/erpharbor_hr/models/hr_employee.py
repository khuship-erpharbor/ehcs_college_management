# coding: utf-8
from datetime import datetime

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    joining_date = fields.Date('Joining Date')
    skype = fields.Char('Skype')

    def action_bd_wishes(self):
        today = datetime.now()
        email_template = self.env.ref('erpharbor_hr.hr_employee_template')
        today_month_day = '%-' + today.strftime('%m') + '-' + today.strftime('%d')
        bd_employees = self.search([('birthday','like',today_month_day)])
        emails = self.search([]).mapped('work_email')
        emails = ','.join(emails)
        for employee in bd_employees:
            email_template.send_mail(employee.id, force_send=True,
                                     email_values={'email_to': emails})
        return True
