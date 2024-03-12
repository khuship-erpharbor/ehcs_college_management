from odoo import models,fields

class Teacherwizard(models.TransientModel):
    _name = "teacher.wizard"
    _description = "This is a wizard which will update the information of staff"
    
    name = fields.Char(string="Teacher Name")
    parent_name = fields.Char(string="Parent Name")
    roll_number = fields.Integer(string="Roll Number")
    dob =  fields.Date(string="Date Of Birth")
    is_teacher =  fields.Boolean(string="Is Teacher ?")
    address = fields.Text("Address")
    gender = fields.Selection([
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
        ],string="Gender")
    
    def action_confirm(self):
        print('\n\n1111111111111111111')
        print('\n\nCONTEXT', self.env.context)
        ctx = self.env.context
        print('ctx', ctx.get('active_id'), ctx.get('active_model'))
        student_id = self.env['college.student'].browse(ctx.get('active_id'))
        print("\n\n\n",student_id)
        student_id.note = 'description'
    
    