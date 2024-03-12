# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    charges_account_id = fields.Many2one('account.account', 'Charges Account',
                                         domain=[('deprecated', '=', False)])
