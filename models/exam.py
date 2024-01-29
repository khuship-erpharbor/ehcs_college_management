from odoo import models,fields,api,_



class Exam(models.Model):
    _name="exam.exam"
    _description="College Exam"
    _rec_name = 'exam_type'

    name = fields.Char(string="Name",default= lambda self:_('New'))

    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('college.exam') or _('New')
        res = super(Exam,self).create(vals)  
        return res


    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    duration = fields.Integer(string="Duration",compute="_compute_duration")
    
    

    # below thing similar with depands also
    @api.onchange('start_date','end_date')
    def _compute_duration(self):
        for remain in self:
            if remain.start_date and remain.end_date:
                remain.duration = abs((remain.start_date - remain.end_date).days)
            else:
                remain.duration = 0

    exam_type = fields.Selection([
        ('internal','Internal'),
        ('external','External')
        ])

    total = fields.Float(string="Total Marks",compute="_compute_total")
    

    exam_line_ids = fields.One2many(
        comodel_name = "exam.exam.line",
        inverse_name = "exam_id",
        string="Exam Line"
        )


    @api.depends('exam_line_ids','exam_line_ids.mark')
    def _compute_total(self):
        for exam in self:
            total = 0
            for el in exam.exam_line_ids:
                print("\n\n\n\nel.examl)id::::::", el.exam_id)
                total += el.mark
            exam.total = total

    

class Examline(models.Model):
    _name = "exam.exam.line"
    _description = "Exam info"

    subject_id = fields.Many2one(
        comodel_name = "college.subject",
        string="Subjects"
        )
    

    exam_id = fields.Many2one(
        comodel_name = "exam.exam",
        string="Exam"
        )
    mark = fields.Float(string="Marks")

    @api.onchange('subject_id')
    def onchange_subject_id(self):
        self.mark = self.subject_id.marks

    
    


            

    




