from odoo import models,fields

class StudentReportWizard(models.TransientModel):
    _name = "student.report.wizard"
    _description = "print student report"

    student_id = fields.Many2one(
        comodel_name = "college.student",
        string = "Student"
        )

    gender = fields.Selection([
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
        ],string="Gender")

    age = fields.Integer(string="Age")

    def action_print_report(self):
        
        selected_student = self.student_id
        students = self.env['college.student'].search_read([])
        data = {
            'form_data': {
                'student_id': selected_student.name,
                'gender':self.gender,
                'age': self.age,
            },

            'students': [{'country':selected_student.country,'course':selected_student.course}],
        }
        print("\n\n\n",data)
        return self.env.ref('college_management.action_report_all_student_list').report_action(self, data=data)



