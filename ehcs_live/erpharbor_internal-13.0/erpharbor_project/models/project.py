# -*- coding: utf-8 -*-

from odoo import models, fields, api
import calendar


class Project(models.Model):
    _inherit = 'project.project'

    def _compute_working_hours(self):
        for project in self:
            project_task = self.env['project.task'].search([('project_id', '=', project.id)])
            total_hours = 0
            for task in project_task:
                total_hours += task.effective_hours
            project.working_hours = total_hours

    @api.depends('planned_hours', 'working_hours')
    def _compute_progress(self):
        for project in self:
            project.project_progress = 0.0
            if project.planned_hours != 0:
                project.project_progress = (project.working_hours * 100) / project.planned_hours

    stage_ids = fields.Many2many('project.task.type', 'project_task_type_rel', 'project_id', 'type_id', string='Stages')
    planned_hours = fields.Float('Initially Planned Hours')
    working_hours = fields.Float('Working Hours', compute="_compute_working_hours")
    project_progress = fields.Float('Project Progress', compute="_compute_progress")
    
    is_project = fields.Boolean(string="Restrict Hours")
    
    def action_project_hours_details(self):
        today = fields.Date.today()
        first_day_of_month = fields.Date.today().replace(day=1)

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
                    mail_template = self.env.ref('erpharbor_project.emp_project_hours_template')
                    print("\n\n\n\nmail template", mail_template)
                    
                    # Send mail only to the project manager
                    mail_template.with_context(ctx).send_mail(project_manager.id, force_send=True)


class ProjectTask(models.Model):
    _inherit = 'account.analytic.line'

    is_invoiced = fields.Boolean('Invoiced', help="It will be checked if task entry is invoiced.")
