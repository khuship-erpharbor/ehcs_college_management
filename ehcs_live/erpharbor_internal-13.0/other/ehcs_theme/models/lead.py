# -*- coding: utf-8 -*-

from odoo import models, fields, api
 
class CrmLead(models.Model):
    _inherit = 'crm.lead'

    requirement_ids = fields.Many2many('project.requirement',
                                       string='Requirement')
    company_name = fields.Char('Company Name')
    company_website = fields.Char('Company Website')
    skype = fields.Char('Skype')
    #    phone_code_id = fields.Many2one('phone.country.code', 'Phone Code')
    budjet_id = fields.Selection([('1k_to_5k', 'Below $5k'),
                                  ('5k_to_15k', '$5k - $15k'),
                                  ('15k_to_40k', '$15k - $40k'),
                                  ('40k_to_60k', '$40k - $60k'),
                                  ('60k', 'Above $60k')], 'Project Budget')


class ProjectRequirement(models.Model):
    _name = 'project.requirement'
    _description = 'Project Requirement'

    name = fields.Char('Requirement')
