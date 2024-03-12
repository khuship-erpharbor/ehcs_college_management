from odoo import models,fields,api
from datetime import datetime
from odoo.exceptions import ValidationError

class Salary(models.Model):
    _name="college.salary"
    _description="College Salary"
    _rec_name = "tech_amount"

    start_date = fields.Date(string="Date")

    @api.constrains('start_date')
    def _check_start_date(self):
        for rec in self:
            today = datetime.now().date()
            print("\n\n\n\ntoday...........",today)
            if rec.start_date != today:
                raise ValidationError("Enter today date")

   
    tech_amount = fields.Float(string="Amount")
    user_id = fields.Many2one(
        comodel_name="res.users",
        string = "Responsible",
        groups = "college_management.group_college_teacher",
        )

    salary_id = fields.Many2one(
        comodel_name = "college.teacher",
        string="Salary"
        )
    
   



    

    
    



