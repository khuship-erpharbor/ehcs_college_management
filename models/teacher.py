from odoo import models,fields,api, _
from datetime import datetime,date
from odoo.exceptions import ValidationError

class Teacher(models.Model):
    _name = "college.teacher"
    _description = "Teacher Info"

    tech_ref = fields.Char(string="Teacher Ref", default=lambda self: _('New'))
    @api.model
    def create(self,vals):
        if vals.get('tech',_('New')) == ('New'):
            vals['tech_ref'] = self.env['ir.sequence'].next_by_code('college.teacher') or _('New')
        res = super(Teacher,self).create(vals) 
        res['qualification'] = 'B.SC.IT' 
        return res 

    name = fields.Char(string="Teacher Name")
    def name_get(self):
        teacher_list = []
        for record in self:
            name = record.tech_ref + record.name
            teacher_list.append((record.id,name))
        return teacher_list
    ref = fields.Char(string="Reference")
    age = fields.Integer(string="Age")
    is_teacher = fields.Boolean(string="Is Teacher?")

    def unlink(self):
        if self.is_teacher != True:
            raise ValidationError("If teacher then only allowed")
        return super(Teacher,self).unlink()

    degree = fields.Char(string="Degree",compute="_compute_degree")
    @api.depends('age')
    def _compute_degree(self):
        for rec in self:
            if rec.age  >= 18 and rec.age < 22:
                rec.degree = 'Graduate'
            elif rec.age > 21:
                rec.degree = 'Post Graduate'
            else:
                rec.degree = 'School'


    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    duration = fields.Integer(string="Duration",compute="_compute_duration")
    leave = fields.Integer(string="Leave")
    salary = fields.Float(string="Salary",compute="_compute_salary")
    
    @api.depends('start_date','end_date')
    def _compute_duration(self):
        for remain in self:
            if remain.start_date and remain.end_date:
                remain.duration = abs((remain.start_date - remain.end_date).days)
            else:
                remain.duration = 0
    
    @api.depends('leave')
    def _compute_salary(self):
        for package in self:
            if package.leave >= 10:
                package.salary = 25000
            elif package.leave >= 5:
                package.salary = 32000
            else:
                package.salary = 45000



    gender = fields.Selection([
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
        ],string="Gender")
    birthdate = fields.Date(string="Birth Date")
    qualification = fields.Char(string="Qualification")
    
    def write(self,vals):
        if vals.get('subject_id') == 'python':
            self.qualification = 'B.sc.IT'
        res = super(Teacher,self).write(vals)
        return res

    current_time = fields.Datetime(string="Time",default=datetime.now())
    description = fields.Text(string="Description")

    @api.onchange('subject_id')
    def _subject_id(self):
        if self.subject_id:
            if self.subject_id.description:
                self.description = self.subject_id.description
        else:
            self.description = ''


    student_id = fields.One2many(
        comodel_name = "college.student",
        inverse_name = "teacher_id",
        string="Student"
        )

    
    subject_id = fields.Many2one(
        comodel_name = "college.subject",
        string = "Subject"
        )
    
