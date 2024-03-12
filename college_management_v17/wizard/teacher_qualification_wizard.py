from odoo import models,fields

class Qualificationwizard(models.TransientModel):
	_name = "teacher.qualification.wizard"
	_description = "Qualification Update"


	qualification = fields.Char(string="Qualification")


	def update_qualification(self):
		ctx = self.env.context
		if ctx.get('active_ids'):
			qualification_id = self.env['college.teacher'].browse(ctx.get('active_ids'))
			qualification_id.qualification = self.qualification
