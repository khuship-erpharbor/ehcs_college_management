# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_reconciled_info_JSON_values(self):
        reconciled_lst = super(AccountMove, self)._get_reconciled_info_JSON_values()
        payment_obj = self.env['account.payment']
        currency_obj = self.env['res.currency']
        for reconciled_vals in reconciled_lst:
            payment_rate = 0
            if reconciled_vals.get('account_payment_id'):
                payment_rate = payment_obj.browse(reconciled_vals.get('account_payment_id')).currency_rate
                if payment_rate:
                    reconciled_vals.update({'currency_rate': payment_rate})
            if payment_rate == 0 and reconciled_vals.get('date'):
                reconciled_vals.update({
                    'currency_rate': currency_obj._get_conversion_rate(self.currency_id, self.company_id.currency_id, self.company_id, reconciled_vals.get('date'))
                })
        return reconciled_lst
