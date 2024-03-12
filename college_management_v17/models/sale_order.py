from odoo import models,fields,api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_sale_order = fields.Boolean(string="Is saleorder?")
    
    product_id = fields.Many2one(
        comodel_name = "product.template",
        string = "Products"
        )
    
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

    def action_product(self):
        res = {
                'name':('Productwizard'),
                'type':'ir.actions.act_window',
                'res_model':'product.product',
                'view_id': self.env.ref('college_management.product_wizard_form_view').id,
                'view_mode':'form',
                'view_type':'form',
                'target':'new'
        }
        return res

    def action_send_mail(self):
        template_id = self.env.ref('college_management.sale_order_email_template').id
        template = self.env['mail.template'].browse(template_id)
        attachment= self.env['ir.attachment'].search([('res_model','=','sale.order'),('res_id','=',self.id)])
        template.send_mail(self.id, force_send=True,email_values={'attachment_ids': [(6, 0, attachment.ids)]})
    
    def unlink(self):
        for rec in self: 
            if rec.state == 'cancel':
                raise UserError("This transaction cannot be deleted sorry")
            return super(SaleOrder,self).unlink()
        

    def action_purchase_order(self):
        purchase_order = self.env['purchase.order'].create({
            'partner_id': self.partner_id.id,
            'sale_order_id': self.id
        })
        print("\n\n\nres...........", purchase_order)

        for sale_order_line in self.order_line:
            purchase_order_line = self.env['purchase.order.line'].create({
                'order_id': purchase_order.id,
                'product_id': sale_order_line.product_id.id,
                'price_unit':sale_order_line.price_unit,
            })
            print("\n\n\npurchase order line.......", purchase_order_line)
            

    partner_count = fields.Integer(string="Customer",compute="_compute_partner_count")

    def _compute_partner_count(self):
        for rec in self:
            rec.partner_count = self.env['purchase.order'].search_count([('sale_order_id','=',rec.id)])


    def action_open_purchase_order(self):
        return {
            'type':'ir.actions.act_window',
            'name':'Purchase Order',
            'res_model':'purchase.order',
            'domain':[('sale_order_id','=',self.id)],
            'view_mode':'tree,form',
            'target':'current'
        }      

    purchase_order_id = fields.Many2one('purchase.order')


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_sale_order_line = fields.Boolean(string="Saleorder")
  


class ProductTemplate(models.Model):
    _inherit = "product.template"

    customer_count = fields.Integer(string="Customer",compute="_compute_customer_count")

    def _compute_customer_count(self):
        for rec in self:
            rec.customer_count = self.env['sale.order'].search_count([('product_id','=',rec.id)])
    

    def action_open_customers(self):
        return {
            'type':'ir.actions.act_window',
            'name':'Products',
            'res_model':'sale.order',
            'view_mode':'tree,form',
            'domain':[('product_id','=',self.id)],
            'target':'current',
        }

# class PurchaseOrder(models.Model):
#     _inherit = "purchase.order"

#     sale_order_id = fields.Many2one('sale.order')

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, order=None):
        args = args or []
        domain = []
        if name:
            domain = ['|','|',('name',operator,name),('phone',operator,name),('email',operator,name)]
        return self._search(domain + args, limit=limit, order=order)    
    
    @api.model_create_multi
    def create(self,vals_list):
        res = super(ResPartner,self).create(vals_list)
        res['function'] = 'Marketing Director'
        return res

