from odoo import models,fields

class Cancelwizard(models.TransientModel):
    _name = "college.student.cancel"
    _description = "cancellation info"

    name = fields.Char(string="Reason",required=True)

    def action_confirm(self):
        ctx = self.env.context
        print("\n\n\n",ctx)
        if ctx.get('active_id'):
            student_id = self.env['college.student'].browse(ctx.get('active_id'))
            student_id.cancellation_reason = self.name
            student_id.action_confirm()




   