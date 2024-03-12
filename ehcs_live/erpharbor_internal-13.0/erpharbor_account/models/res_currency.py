# -*- coding: utf-8 -*-
from odoo import api, models


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    @api.model
    def _get_conversion_rate(self, from_currency, to_currency, company, date):
        if self._context.get('currency_rate'):
            return self._context.get('currency_rate')
        return super(ResCurrency, self)._get_conversion_rate(from_currency, to_currency, company, date)
