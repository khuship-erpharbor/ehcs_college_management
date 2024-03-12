from odoo import models,fields

class Coursewizard(models.TransientModel):
    _name = "student.course.wizard"
    _description = "course info"

    course = fields.Char(string="Course")


    def update_course(self):
        ctx = self.env.context
        print("\n\n\n",ctx)
        if ctx.get('active_ids'):
            course_id = self.env['college.student'].browse(ctx.get('active_ids'))
            course_id.course = self.course
