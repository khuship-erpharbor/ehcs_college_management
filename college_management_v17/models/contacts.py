from odoo import models,fields

class Contacts(models.Model):
    _inherit = "res.partner"

    subject_id = fields.Many2one(
        comodel_name="college.subject",
        string="Subject"
        )
    sub_ids = fields.Many2many('college.subject')


    def action_add_subject(self):
        subj_obj = self.env["college.subject"]

        sub_id = [2]

        subj_recordset = subj_obj.browse(sub_id)
        print ("\n\nsubj recordset.......    ", subj_recordset, subj_recordset.exists())

        subjs = subj_obj.search([('name','ilike','python')])
        print ("\n\n\n\nsubjs....", subjs)
        for partner in self:
            for subj in subjs:
                partner.write({'sub_ids':[(4,subj.id)]})
        return True
    
    def action_update_subject(self):
        subj_obj = self.env['college.subject']
        subjs = subj_obj.search([('name','ilike','python')])
        print("\n\n\n\nsubjects",subjs)
        for partner in self:
            print("\n\n\n\npartnmer::::::::", partner)
            for subj in subjs:
                partner.write({'sub_ids':[(1,subj.id,{'description':'PY'})]})
        return True
   
    def action_remove_subject_database(self):
        subj_obj = self.env['college.subject']
        subjs = subj_obj.search([('name','ilike','python')])
        print("\n\n\n\nsubj:::",subjs)
        for partner in self:
            for subj in subjs:
                partner.write({'sub_ids':[(2,subj.id)]})
        return True

    def action_remove_subject(self):
        subj_obj = self.env['college.subject']
        subjs = subj_obj.search([('name','ilike','python')])
        print("\n\n\n\nsubj:::",subjs)
        for partner in self:
            for subj in subjs:
                partner.write({'sub_ids':[(3,subj.id)]})
        return True

    def action_remove_all_subject(self):
        for partner in self:
            partner.write({'sub_ids': [(5, 0, 0)]})
        return True
    
    def action_add_contact(self):
        for partner in self:
            partner.create([{
                    'name':'Khushi Patel'
                },
                {
                    'name':'Sakshi Shah'
                }])
            return True