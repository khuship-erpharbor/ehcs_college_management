from odoo import models, fields,api
from datetime import date,timedelta

class Employees(models.Model):
    _inherit = "hr.employee"

    @api.model
    def action_attendence_timesheet_details(self):
        analytic_line_obj = self.env['account.analytic.line']
        attendance = self.env['hr.attendance']
        leave = self.env['hr.leave.report']

        mail_template = self.env.ref(
            'attendence_timesheet_management.emp_attendance_timesheet_email_template'
        )
        # current_date = fields.Date.today()
        previous_date = fields.Date.today() - timedelta(days=1)

        for employee in self.search([('work_email', '!=', False)]):
            leave_records = leave.search([
                ('employee_id', '=', employee.id),
                ('date_from', '<=', f'{previous_date} 00:00:00'),
                ('date_to', '>=', f'{previous_date} 23:59:59'),
            ])
        if not leave_records:
            attendance_records = attendance.search([
                ('employee_id', '=', employee.id),
                ('check_in', '>=', f'{previous_date} 00:00:00'),
                ('check_in', '<=', f'{previous_date} 23:59:59'),

            ])
            print("\n\ndd.........", f'{previous_date} 00:00:00', f'{previous_date} 23:59:59')

            total_attendance_hours = sum(attendance_records.mapped('worked_hours'))

        if not leave_records:
            timesheet_records = analytic_line_obj.search([
                ('employee_id', '=', employee.id),
                ('date', '=', previous_date)
            ])

            total_timesheet_hours = sum(timesheet_records.mapped('unit_amount'))

            remaining_hours = total_attendance_hours - total_timesheet_hours

            print("\n\nAttendance Hours:", int(total_attendance_hours))
            print("Timesheet Hours:", int(total_timesheet_hours))
            print("Remaining Hours:", int(remaining_hours))
            
            if total_timesheet_hours < 8 or total_attendance_hours < 8:
                ctx = {
                    'attendance_hrs': total_attendance_hours,
                    'timesheet_hrs': total_timesheet_hours,
                    'previous_date': previous_date,
                    'remaining_hours': remaining_hours,
                }
                mail_template.with_context(ctx).send_mail(employee.id, force_send=True)
