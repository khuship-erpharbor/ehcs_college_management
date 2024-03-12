from odoo import models,fields,api, _
from datetime import datetime,date
from odoo.exceptions import ValidationError

class Teacher(models.Model):
    _name = "college.teacher"
    _description = "Teacher Info"
    _rec_name = "qualification"
    _inherit =["mail.thread","mail.activity.mixin"]
     
    
    tech_ref = fields.Char(string="Teacher Ref", default=lambda self: _('New'))
    @api.model
    def create(self,vals):
        if vals.get('tech',_('New')) == ('New'):
            vals['tech_ref'] = self.env['ir.sequence'].next_by_code('college.teacher') or _('New')
        res = super(Teacher,self).create(vals) 
        res['qualification'] = 'B.SC.IT' 
        print("\n\n\n\n Teacher Profile",vals)
        return res 
    
    name = fields.Char(string="Teacher Name")
    #display_name = fields.Char(string="Display Name",compute = "_compute_display_name")
    
    @api.depends('name','age')
    def _compute_display_name(self):
        for record in self:
            if record.name and record.age:
                record.display_name = f"{record.name} / {record.age}"
            else:
                record.display_name = f"{record.gender}"
    ref = fields.Char(string="Reference")
    age = fields.Integer(string="Age")
    email_id = fields.Char(string="Email")
    pic = fields.Image(string="Upload Image")
    student_exam_id = fields.Many2one(
        comodel_name = 'exam.exam',
        string= "Student's exam"
        )
    percentage = fields.Float(string="Percentage",related="student_exam_id.percentage")


    is_teacher = fields.Boolean(string="Is Teacher?")
    
    def unlink(self):
        for teacher in self:
            if teacher.is_teacher is True:
                raise ValidationError("If teacher then only allowed")
        return super(Teacher, self).unlink()

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
    wages = fields.Float(string="Wages",compute="_compute_wages")
    
    @api.depends('start_date','end_date')
    def _compute_duration(self):
        for remain in self:
            if remain.start_date and remain.end_date:
                remain.duration = abs((remain.start_date - remain.end_date).days)
            else:
                remain.duration = 0
    
    @api.depends('leave')
    def _compute_wages(self):
        for package in self:
            if package.leave >= 10:
                package.wages = 25000
            elif package.leave >= 5:
                package.wages = 32000
            else:
                package.wages = 45000


    gender = fields.Selection([
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
        ],string="Gender")
    birthdate = fields.Date(string="Birth Date")
    qualification = fields.Char(string="Qualification")
    
    def write(self, vals):
        if 'subject_id' in vals and vals['subject_id'] == 'python':
            self.qualification = 'B.sc.IT'
        res = super(Teacher, self).write(vals)
        print("\n\n\n\n teacher write method vals",vals)
        return res


    current_time = fields.Datetime(string="Time",default=datetime.now())
    description = fields.Text(string="Description")
    
    def action_salary(self):
        # if not self.salary_line_ids:  
        res = {
                'name':('Salarywizard'),
                'type':'ir.actions.act_window',
                'res_model':'college.student.salary',
                'view_id': self.env.ref('college_management.college_student_salary_form_view').id,
                'view_mode':'form',
                'view_type':'form',
                'target':'new'
        }
        return res

    @api.onchange('subject_id')
    def _subject_id(self):
        if self.subject_id:
            if self.subject_id.description:
                self.description = self.subject_id.description
        else:
            self.description = ''


    student_ids = fields.One2many(
        comodel_name = "college.student",
        inverse_name = "teacher_id",
        string="Student"
        )

    student_id = fields.Many2one(
        comodel_name = "college.student",
        string = "Student"
        )

    salary_line_ids = fields.One2many(
        comodel_name = "college.salary",
        inverse_name = "salary_id",
        string="Salary"
        )
    subject_id = fields.Many2one(
        comodel_name = "college.subject",
        string = "Subject"
        )

    
    subject_ids = fields.Many2many(
        comodel_name="college.subject",
        relation = "teacher_subject_rel",
        column1 = "teacher_id",
        column2 = "subject_id",
        string="Subjects"
        )
        
    
    def action_send_mail(self):
        template_id = self.env.ref('college_management.college_teacher_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id,force_send=True)

    @api.model
    def _name_search(self,name,args=None,operator="ilike",limit=100,order=None):
        args = args or []
        domain = []
        if name:
            domain = ['|','|',('name',operator,name),('email_id',operator,name),('ref',operator,name)]
        return self._search(domain + args,limit=limit,order=order)

    #Special Commands

    def specialcommand0(self):
        self.create({"name":"Khushi College", "student_ids":[(0,0,{'name':"Khushi Student 1","ref":1}),
                                                            (0,0,{'name':"Khushi Student 2","ref":2}),
                                                            (0,0,{'name':"Khushi Student 3","ref":3}),
                                                            (0,0,{'name':"Khushi Student 4","ref":4}),
                                                            (0,0,{'name':"Khushi Student 5","ref":5})]})

        self.write({"student_ids": [[0,0,{'name':'Khushi college 6'}]]})
    
    def specialcommand1(self):
        #we can use this command while doing update operation for parent and child model
        vals = {'student_ids':[]}
        for student in self.student_ids:
            vals['student_ids'].append([1,student.id,{'name': student.name + "Name",
                                                      'address':"Ganpat University"}])
        self.write(vals)

    def specialcommand2(self):
        self.write({'student_ids':[(2, 70, 0),(2, 72, 0)]})

    def specialcommand3(self):
        self.write({'student_ids':[(3, 104, False)]})


    def specialcommand4(self):
        self.write({'student_ids':[(4, 93, 0)]})

    def specialcommand5(self):
        self.write({'student_ids':[(5,0,0)]})

    def specialcommand6(self):
        ids = [3,14,15]
        self.write({'student_ids':[(6,0,ids)]})
    # def action_add_teacher(self):
    #     for teacher in self:
    #         teacher.create([{
    #             'name': 'Feny Patel',
    #             'student_id': teacher.id,
    #         },
    #         {
    #             'name': 'Priti Patel',
    #             'student_id': teacher.id,
    #         }])
    #     return True

     

      

