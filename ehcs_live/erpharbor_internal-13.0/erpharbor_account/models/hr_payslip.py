# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    net_salary = fields.Float(compute='_compute_net_salary', store=True)

    @api.depends('line_ids', 'line_ids.total')
    def _compute_net_salary(self):
        for payslip in self:
            payslip.net_salary = sum(payslip.line_ids.filtered(
                lambda x: x.code == 'NET'
            ).mapped('total'))
        return True
