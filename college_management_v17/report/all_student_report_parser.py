from odoo import models,fields,api

class AllStudentReport(models.AbstractModel):
	_name = "report.college_management.report_all_student_list"
	_description = "Student Report"

	@api.model
	def _get_report_values(self, docids ,data=None):
		print("\n\n\n",data)
		docs = self.env['college.student'].browse(docids)
		print("\n\n\n",docs)
		return {
			'docs' : docs,
			'doc_ids' : docids,
            'doc_model' : self.env['college.student'],
            'data' : data,
            'context': self.env.context,
		}





