from odoo import models,fields,api,_


class Subject(models.Model):
    _name="college.subject"
    _description="College Subjects"

    ref = fields.Char(string="Reference", default=lambda self: _('New'))

    @api.model
    def create(self,vals):
        if vals.get('ref',_('New')) == _('New'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('college.subject') or _('New')
        res = super(Subject,self).create(vals)
        return res     






    name = fields.Char(string="Subject name")
    description = fields.Text(string="Description")
    marks = fields.Float(string="Marks")
    
    
 
    
    



