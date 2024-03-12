from odoo import models, fields

class Salesproduct(models.TransientModel):
    _name = "college.student.product"
    _description = "product info"

    product_ids = fields.Many2many(
        comodel_name="product.product",
        relation="sale_product_rel",
        string="Product"
    )


    def action_submit(self):
        ctx = self.env.context
        print("\n\n\n", ctx)

        
        #for product in self.product_ids
    
        if ctx.get('active_model') == 'sale.order':
            so = self.env['sale.order'].browse(ctx.get('active_id'))
            sol = self.env['sale.order.line'].create([
                {
                    'order_id': so.id,
                    'product_id': product.id,
                }  for product in self.product_ids
            ])
            

            return {
                'name': 'Sale Order Line',
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order.line',
                'view_mode': 'tree,form',
                'domain': [('id','in',sol.ids)],
            }

 
        elif ctx.get('active_model') == 'purchase.order':

            po = self.env['purchase.order'].browse(ctx.get('active_id'))
            
            
            pol = self.env['purchase.order.line'].create([
                {
                    'order_id':po.id,
                    'product_id':product.id,
                } for product in self.product_ids

                ]) 
            return {
            'name': 'purchase Order Line',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order.line',
            'view_mode': 'tree,form',
            'domain': [('id','in',pol.ids)],
            }
            





                



















        
    




   

    