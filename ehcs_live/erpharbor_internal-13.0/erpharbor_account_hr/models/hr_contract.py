# -*- coding: utf-8 -*-
from odoo import fields, models


class Contract(models.Model):
    _inherit = 'hr.contract'

    deduction = fields.Monetary('Deduction', required=True, default=2000)
