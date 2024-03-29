# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    gst_account_id = fields.Many2one('account.account', 'GST Account',
                                     domain=[('deprecated', '=', False)])
