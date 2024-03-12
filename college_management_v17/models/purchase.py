from odoo import models,fields
from datetime import date
from dateutil.relativedelta import relativedelta

class Purchase(models.Model):
    _inherit = "purchase.order"

    is_purchase_order = fields.Boolean(string="Is Purchaseorder?")
    emi_line_ids = fields.One2many(
        comodel_name = "emi.line",
        inverse_name = "purchase_id",
        string="EMI"
        )
    

    month = fields.Integer(string="Months")

    def action_emi(self):
        if not self.is_purchase_order:
            self.is_purchase_order = True
            amount = self.amount_total/self.month
            for amount_total in range(self.month):
                emi_line = self.env['emi.line'].create({'date':self.date_approve + relativedelta(months=amount_total),'amount':amount,'purchase_id':self.id})
                print("\n\n\n\n",self.amount_total)
            return emi_line 

   
    def action_sale_order(self):
        sale_order = self.env['sale.order'].create(
            {
                'partner_id': self.partner_id.id,
                'purchase_order_id':self.id,
            })
        for purchase_order_line in self.order_line:
            sale_order_line = self.env['sale.order.line'].create(
                {
                    'order_id':sale_order.id,
                    'product_id':purchase_order_line.product_id.id
                })
    
    partner_count = fields.Integer(string="Customers",compute="_compute_partner_count")
        
    def _compute_partner_count(self):
        for rec in self:
            rec.partner_count = self.env['sale.order'].search_count([('purchase_order_id','=',rec.id)])


    def action_open_sale_order(self):
        return {
            'type':'ir.actions.act_window',
            'name':'Sale Order',
            'res_model':'sale.order',
            'domain':[('purchase_order_id','=',self.id)],
            'view_mode':'tree,form',
            'target':'current'
        }  

    sale_order_id = fields.Many2one('sale.order')  

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    image = fields.Binary(string="Image", related='product_id.image_1920')

class Emiline(models.Model):
    _name = "emi.line"

    date = fields.Date(string="Date")
    amount = fields.Float(string="Amount")
    purchase_id = fields.Many2one(
        comodel_name = "purchase.order",
        string="purchase"
        )


