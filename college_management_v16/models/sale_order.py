from odoo import models,fields,api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_sale_order = fields.Boolean(string="Is saleorder?")
    
    confirm = fields.Char(string="Confirm Reason")

    #when clicking on confirm button message appears in confirm label
    
    def action_confirm(self):
        self.confirm = "Confirmation done"
        return super(SaleOrder,self).action_confirm()

# clicking on check button new record create in college mangement-> student 
    def action_check(self):
        self.is_sale_order = True
        student_list = {
            'ref': 'Karishma'
        }
        student = self.env['college.student'].create(student_list)
        

        
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_sale_order_line = fields.Boolean(string="Saleorder")


class ProductTemplate(models.Model):
    _inherit = "product.template"