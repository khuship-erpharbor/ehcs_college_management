from odoo import models,fields,api, _
from datetime import date

class Student(models.Model):
    _name = "college.student"
    _description = "Student Information"

    name = fields.Char(string="Student Name",required=True,help="Enter your name", default=lambda self: _('New'))
    ref = fields.Char(string="Reference")
    birthdate = fields.Date(string="Birth Date")
    age = fields.Integer(string="Age",compute="_compute_age", store=True)
    @api.depends('birthdate')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.birthdate:
                rec.age = today.year - rec.birthdate.year
            else:
                rec.age = 0

    is_student = fields.Boolean(string="Is Student?",default=True)

    @api.onchange('is_student')
    def onchange_student(self):
        if self.is_student == True:
            self.teacher_id = ''


    marks = fields.Float(string="Marks")
    address = fields.Text(string="Address")
    country = fields.Char(string="Country")

    def copy(self,default="none"):
        res = super(Student,self).copy(default={'country':'India'})
        return res
    
    #  orm create method
    # @api.model_create_multi
    # def create(self,vals_list):
    #     res = super(Student,self).create(vals_list)
    #     res['address'] = 'Bodakdev'
    #     return res

    gender = fields.Selection([
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
        ],string="Gender")
    note = fields.Html(string="Note", help="Please write simple note",readonly=True)
    nickname = fields.Char(string="Nickname")
    
    # orm create method
    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('college.student') or _('New')
        res = super(Student,self).create(vals)
        # res['address'] = 'Bodakdev'
        return res




    parent_name = fields.Char(string="Parent Name")
    status = fields.Selection([
        ('regular','Regular'),
        ('external','External')
        ],string="Status")
    placement = fields.Selection([
        ('intern','Internship'),
        ('job','Job')
        ],string="Placement")
    stipend = fields.Float(string="Stipend")
    salary = fields.Float(string="Salary")
    
    state = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('done','Done'),
        ('cancel','Cancelled')
        ])
    def action_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        self.state = 'confirm'
        self.teacher_id = ''

    # orm search method

    def action_search(self):
        # clicking on search button in tree view any male then uncheck is_student boolean
        male_students = self.search([('gender','=','male')])
        print("\n\n\nmale students...",male_students)
        student = male_students.write({'is_student':False})
        teacher = self.env['college.teacher'].create({'name':'kinnari'})

        students = self.env['college.student'].search([])
        print("\n\n\n\n\nstudents...",students)

        # search for and 
        female_students = self.env['college.student'].search([('gender','=','female'),('age','>', 20)])
        print("\n\n\nfemale students above 20 and...",female_students)
        #search for or
        female_students_or = self.env['college.student'].search(['|',('gender','=','female'),('age','>', 20)])
        print("\n\n\nfemale students above 20 or...",female_students_or)
   
    # orm search count
            
        student_count = self.env['college.student'].search_count([])
        print("\n\n\nstudent counts...",student_count)
        female_students_count = self.env['college.student'].search_count([('gender','=','female'),('age','>', 20)])
        print("\n\n\nfemale students counts and...",female_students_count)
        female_students_count_or = self.env['college.student'].search_count(['|',('gender','=','female'),('age','>', 20)])
        print("\n\n\nfemale students above 20 or...",female_students_count_or)
   
   # orm read method
        students_list = self.env['college.student'].read([])
        print("\n\n\n\n\nstudents read...",students_list)
            
    # orm write method
    def write(self, vals):
        print("\n\n\n\nvals",vals)
        if vals.get('state') == 'confirm':
            self.teacher_id = ''
        if vals.get('is_student') == True:
            self.address = 'Ganpat University'
        
        res = super(Student,self).write(vals)
        return res




    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'


    teacher_id = fields.Many2one(
        comodel_name = "college.teacher",
        string="Teacher",
        domain=[('gender','=','female')]
        )

    @api.onchange('teacher_id')
    def onchange_teacher_id(self):
        if self.teacher_id.gender:
            self.gender = self.teacher_id.gender
        else:
            self.gender = ''

    @api.onchange('teacher_id')
    def onchange_teacher(self):
        if self.teacher_id.age:
            self.age = self.teacher_id.age
        else:
            self.age = ''


    @api.onchange('gender')
    def onchange_gender(self):
        if self.gender == 'other':
            self.is_student = False
        else:
            self.is_student = True


    
    subject_id = fields.Many2many(
        comodel_name="college.subject",
        relation = "student_subject_rel",
        column1 = "student_id",
        column2 = "subject_id",
        string="Subjects"
        )
    # name_get but not possible in odoo 17
    # def name_get(self):
    #     teacher_list = []
    #     for record in self:
    #         print("\n\n\n\n\n:::",self)
    #         name = record.ref + record.name
    #         teacher_list.append((record.id,name))
    #     return teacher_list