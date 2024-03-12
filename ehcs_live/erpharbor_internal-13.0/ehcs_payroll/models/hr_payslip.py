import xmlrpc.client

from odoo import fields, models


class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    def action_fetch_data(self):
        url2 = "https://pms.erpharbor.in"
        db2 = "pms"
        username2 = 'admin'
        password2 = ''
        common2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url2))
        version2 = common2.version()
        uid2 = common2.authenticate(db2, username2, password2, {})

        models2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url2))
        hr_payslip_line = self.env['hr.payslip.worked_days']
        for payroll in self.slip_ids:
            leave_data = models2.execute_kw(db2, uid2, password2, 'hr.leave', 'search_read',
                        [[('employee_id.work_email', '=', payroll.employee_id.work_email),
                         ('holiday_status_id', 'in', ('Unpaid','Sick Time Off')),
                         ('request_date_from', '>=', payroll.date_from),
                         ('request_date_to', '<=', payroll.date_to)]],
                        {'fields': ['number_of_days', 'employee_id', 'holiday_status_id', 'number_of_hours_display']})
            num_of_days = sum(l['number_of_days'] for l in leave_data)
            num_of_hours = sum(l['number_of_hours_display'] for l in leave_data)
            if leave_data:
                # existing line deleted & new created
#                 payroll.worked_days_line_ids.unlink()
                hr_payslip_line.create({
                    'payslip_id': payroll.id,
                    'name': self.env.ref('hr_holidays.holiday_status_unpaid').name,
                    'code': 'UL',
                    'number_of_days': num_of_days,
                    'number_of_hours': num_of_hours,
                    'contract_id': payroll.contract_id.id,
                })





