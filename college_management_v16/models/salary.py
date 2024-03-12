from odoo import models,fields
from datetime import datetime

class Salary(models.Model):
    _name="college.salary"
    _description="College Fees"
    _rec_name = "tech_amount"

    start_date = fields.Date(string="Date")
    tech_amount = fields.Float(string="Amount")

    salary_id = fields.Many2one(
        comodel_name = "college.teacher",
        string="Salary"
        )
    
   



    

    
    



