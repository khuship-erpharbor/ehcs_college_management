from odoo import models, fields, api

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    @api.model
    def send_attendance_reminder_emails(self):
        # Get all employees
        employees = self.env['hr.attendance'].search([])

        # Iterate through each employee
        for employee in employees:
            # Check if there is no attendance for today
            if not self.search([('employee_id', '=', employee.employee_id.id), ('check_in', '>=', fields.Datetime.now().replace(hour=0, minute=0, second=0)), ('check_out', '=', False)]):
                # Send an email to the employee
                self.send_attendance_reminder_email(employee)

    @api.model
    def send_attendance_reminder_email(self, employee):
        # Customize the email content and recipients
        subject = "Attendance Reminder"
        body = f"Dear {employee.employee_id.name},\n\nYou haven't recorded attendance for today. Please make sure to check in/out.\n\nBest Regards,\nHR Department"
        recipient = employee.employee_id.user_id.partner_id.email

        # Send the email
        self.env['mail.mail'].create({
            'subject': subject,
            'body_html': body,
            'email_from': 'khushipatel7363@gmail.com',
            'email_to': recipient,
            'auto_delete': True,
        }).send()

    # You can schedule this method to run daily using a scheduled action
