from odoo import models,fields,api,_
from datetime import datetime

class Fees(models.Model):
    _name="college.fees"
    _description="College Fees"


    name = fields.Char(string="Name", default=lambda self:_('New'))

    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == ('New'):
            vals['name']=self.env['ir.sequence'].next_by_code('college.fees') or _('New')
        res = super(Fees,self).create(vals)
        return res
    today_date = fields.Date(string="Date",default=datetime.now())

    student_id = fields.Many2one(
        comodel_name = "college.student",
        string = "Student Name"
        )

    fees_line_ids = fields.One2many(
        comodel_name = "college.fees.line",
        inverse_name = "fees_id",
        string = "Fees"
        )

    total_fees = fields.Float(string="Total_fees",compute="_compute_total")
    tax_amount = fields.Float(string="Tax Amount",compute="_compute_total")
    total = fields.Float(string="Total",compute="_compute_total")
    
    @api.depends('fees_line_ids','fees_line_ids.price','fees_line_ids.tax','fees_line_ids.sub_total')
    def _compute_total(self):
        for totalsum in self:
            total_fees=0
            tax_amount=0 
            total= 0
            for fl in totalsum.fees_line_ids:
                total_fees += fl.price
                tax_amount += fl.tax
                total += fl.sub_total
            totalsum.total_fees = total_fees
            totalsum.tax_amount = tax_amount
            totalsum.total = total


class Feesline(models.Model):
    _name = "college.fees.line"
    _description="fees info"

    fees_id = fields.Many2one(
        comodel_name = "college.fees",
        string="Fees"
        )
    name = fields.Char(string="Name")
    price = fields.Float(string="Price")
    tax = fields.Float(string="Tax")
    sub_total = fields.Float(string="Sub Total",compute="_compute_subtotal")
    
    @api.depends('price','tax')
    def _compute_subtotal(self):
        for fees in self:
            sub_total = (fees.price * fees.tax / 100) + fees.price
            fees.sub_total = sub_total


    




    

    
    



