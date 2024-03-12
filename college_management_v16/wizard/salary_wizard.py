from odoo import models,fields
from datetime import datetime

class Salarywizard(models.TransientModel):
    _name = "college.student.salary"
    _description = "cancellation info"

    date = fields.Date(string="Date")
    amount = fields.Float(string="Amount")
    teacher_id = fields.Many2many(
        comodel_name ="college.teacher",
        rel = "teacher_salary_rel",
        column1 = "teacher_id",
        column2 = "salary_id",
        string = "Teacher"
        )
    # teacher_id = fields.Many2one(
    #     comodel_name = "college.teacher",
    #     string = "teacher"
    #     )


    # def action_add(self):
    #     ctx = self.env.context
    #     if ctx.get('active_id'):
    #         teacher = self.env['college.teacher'].browse(ctx.get('active_id'))
            
    #         salary_line_data = {
    #             'start_date': self.date,
    #             'tech_amount': self.amount,
    #         }
    #         for teacher in teachers:
    #             teacher.write({
    #                 'salary_line_ids': [(0, 0, salary_line_data)]
    #             })
            
    #             salary = self.env['college.salary'].create({
    #                 'start_date': self.date,
    #                 'tech_amount': self.amount,
    #                 'salary_id': teacher.id
    #    

    
    def action_add(self):
        # print("\n\n\n\n",self)
        for salary in self.teacher_id:
            print("\n\n\n\n",salary)
            res = self.env['college.salary'].create({
                'start_date':self.date,
                'tech_amount':self.amount,
                'salary_id':salary.id
                })
            



   