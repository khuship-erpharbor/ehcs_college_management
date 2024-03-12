from odoo import models, fields

class Project(models.Model):
    _inherit = "project.project"

    is_project = fields.Boolean(string="Restrict Hours")
    
    def action_project_hours_details(self):
        today = fields.Date.today()
        first_day_of_month = fields.Date.today().replace(day=1)
        # last_day_of_month = fields.Date.today().replace(day=30)
        
        last_day_of_month = calendar.monthrange(today.year, today.month)[1]
        last_day_of_month = today.replace(day=last_day_of_month)

        current_month_name = today.strftime('%B')

        projects = self.search([('is_project', '=', True)])

        for project in projects:
            planned_hours = project.planned_hours
            threshold_hours = planned_hours * 0.10
            total_planned_hours = planned_hours - threshold_hours
            print("\n\n\n\ntotal planned hours",total_planned_hours)

            total_unit_amount = sum(self.env['account.analytic.line'].search([
                ('project_id', '=', project.id),
                ('date', '>=', first_day_of_month),
                ('date', '<=', last_day_of_month),
            ]).mapped('unit_amount'))

            if total_unit_amount >= total_planned_hours:
                project_manager = project.user_id

                for employee in self.env['account.analytic.line'].search([
                    ('project_id', '=', project.id),
                    ('date', '>=', first_day_of_month),
                    ('date', '<=', last_day_of_month),
                ]).mapped('employee_id'):
                    ctx = {
                        'total_hours': total_unit_amount,
                        'current_month_name': current_month_name,
                        'project_name': project.name,
                    }
                    mail_template = self.env.ref('project_management.emp_project_hours_template')
                    print("\n\n\n\nmail template", mail_template)
                    
                    # Send mail only to the project manager
                    mail_template.with_context(ctx).send_mail(project_manager.id, force_send=True)
