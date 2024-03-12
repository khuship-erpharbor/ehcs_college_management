from odoo import models,fields

class Sports(models.Model):
    _name = "college.sports"
    _description = "Sports Information"


    name = fields.Char(string="Game Name")
    date = fields.Date(string="Date")
    fees = fields.Float(string="Fees")
    active = fields.Boolean(string="Active",default=True)

    sportsform_id = fields.Many2one(
        comodel_name = "college.sportsform",
        string="Form"
        )
    student_count = fields.Integer(string="Students",compute="_compute_student_count")

    def _compute_student_count(self):
        for rec in self:
            rec.student_count = self.env['college.student'].search_count([('game_id','=',rec.id)])
    


  
   