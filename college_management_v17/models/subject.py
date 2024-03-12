from odoo import models,fields,api,_


class Subject(models.Model):
    _name="college.subject"
    _description="College Subjects"

    ref = fields.Char(string="Reference", default=lambda self: _('New'))

    @api.model
    def create(self,vals):
        if vals.get('ref',_('New')) == _('New'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('college.subject') or _('New')
        res = super(Subject,self).create(vals)
        return res     

    
    name = fields.Char(string="Subject name")
    sequence = fields.Integer(string="Sequence")

    _sql_constraints = [
        ('unique_name','unique (name)','Name must be unique.'),
        ('check_sequence','check(sequence > 0)','Sequence must be non positive zero.')
    ]

    #  _sql_constraints = [(
    #     'unique_name', "", "Another entry with the same name already exists.",
    # )]

    description = fields.Text(string="Description")
    marks = fields.Float(string="Marks")

    teacher_count = fields.Integer(string="Teachers", compute="_compute_teacher_count")

    def _compute_teacher_count(self):
        for rec in self:
            teacher_count = self.env['college.teacher'].search_count([('subject_id','=',rec.id)])
            rec.teacher_count = teacher_count    
 
    def action_open_teachers(self):
        return {
            'type':'ir.actions.act_window',
            'res_model':'college.teacher',
            'name':'Teachers',
            'view_mode':'tree,form',
            'domain': [('subject_id','=',self.id)],
            'target':'current',
        }
    



