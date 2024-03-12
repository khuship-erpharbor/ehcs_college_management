# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    user_sync_id = fields.Integer('User Sync Id')


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    task_type_sync_id = fields.Integer('Project Task Type Sync Id')


class Project(models.Model):
    _inherit='project.project'

    project_sync_id = fields.Integer('Project Sync Id')


class ProjectTask(models.Model):
    _inherit='project.task'

    project_task_sync_id = fields.Integer('Project Task Sync Id')


class ResPartner(models.Model):
    _inherit='res.partner'

    partner_sync_id = fields.Integer('Partner Sync Id')
    is_created_with_user = fields.Boolean("Created With User")


class HrDepartment(models.Model):
    _inherit='hr.department'

    hr_dept_sync_id = fields.Integer('HR Department Sync Id')


class HrEmployee(models.Model):
    _inherit='hr.employee'

    hr_employee_sync_id = fields.Integer('HR Employee Sync Id')


class AccountAnalyticLine(models.Model):
    _inherit='account.analytic.line'

    analytic_line_sync_id = fields.Integer('Analytic Line Employee Sync Id')


class MessageFollower(models.Model):
    _inherit='mail.followers'

    follower_sync_id = fields.Integer('Follower Sync Id')


class Attachment(models.Model):
    _inherit='ir.attachment'

    attachment_sync_id = fields.Integer('Attach Sync Id')
