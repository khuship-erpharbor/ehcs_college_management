# coding: utf-8
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    hide_tax = fields.Boolean('Hide Taxes in Report')
