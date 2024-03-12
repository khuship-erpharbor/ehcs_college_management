from odoo import models,fields,api, _
from datetime import date
from odoo.exceptions import UserError


class Student(models.Model):
    _name = "college.student"
    _description = "Student Information"
    _inherit = ["mail.thread","mail.activity.mixin"]
    _rec_name = 'name'

    ref = fields.Char(string="Student Name",required=True,help="Enter your name", default=lambda self: _('New'))
    name = fields.Char(string="name")
    pic = fields.Binary(string="Upload Image")
    # this is display name instead of name get
    display_name = fields.Char(string="Display Name", compute="_compute_display_name", store=True)
    
    @api.depends('name','country')
    def _compute_display_name(self):
        for record in self:
            if record.name and record.country:
                record.display_name = f"{record.name} - {record.country}"
            else:
                record.display_name = f"{record._name}"

    partner_id = fields.Many2one(
        comodel_name = "res.partner",
        string = "Partner"
        )
    
    # order_id = fields.Many2one(
    #     comodel_name = "sale.order",
    #     string = "Order"
    #     )

    # @api.onchange('partner_id')
    # def onchange_partner_id(self):
    #     for rec in self:
    #         return {'domain' : {'order_id' : [('partner_id','=',rec.partner_id.id)]}} 
       
    game_id = fields.Many2one(
        comodel_name="college.sports",
        string = "Game"
        )
    
    email_id = fields.Char(string="Email")
    user_id = fields.Many2one('res.users', 'Partner')
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
        

    # @api.depends('name', 'ref', 'birthdate', 'age')
    # def _compute_display_name(self):
    #     for record in self:
    #         if record.name:
    #             record.display_name = record.name
    #         elif record.ref:
    #             record.display_name = record.ref
    #         elif record.birthdate:
    #             record.display_name = f"Birthdate: {record.birthdate}"
    #         else:
    #             record.display_name = f"{record._name},{record.id}"
    
    is_student = fields.Boolean(string="Is Student?",default=True)

    @api.onchange('is_student')
    def onchange_student(self):
        if self.is_student:
            self.teacher_id = ''


    marks = fields.Float(string="Marks")
    course = fields.Char(string="Course")

    def action_course(self):
        res = {
                'name':('Coursewizard'),
                'type':'ir.actions.act_window',
                'res_model':'student.course.wizard',
                'view_id':self.env.ref('college_management.student_course_wizard_form_view').id,
                'view_mode':'form',
                'view_type':'form',
                'target':'new',
        }

        return res



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
        if vals.get('ref',_('New')) == _('New'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('college.student') or _('New')
        res = super(Student,self).create(vals)
        print("\n\n\n\n Student Profile Vals",vals)
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
    
    cancellation_reason = fields.Char(string="Cancellation Reason")
    
    def action_cancel(self):
         
         res = {
                'name': ('Cancelwizard'),
                'type': 'ir.actions.act_window',
                'res_model': 'college.student.cancel',
                'view_id': self.env.ref('college_management.college_student_cancel_form_view').id,
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new',
            }
           
         return res

    state = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('done','Done'),
        ('cancel','Cancelled')
        ])
    def action_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        self.state = 'cancel'
        self.teacher_id = ''
    
    def action_done(self):
        self.state = 'done'

    def unlink(self):
        for record in self:    
            if record.state == 'done':
                raise UserError("This transaction cannot be deleted")
            return super(Student,self).unlink()



    def action_teacher(self):
        # action = self.env.ref('college_management.action_teacher_wizard').read()[0]
        res = {
                'name': ('Wizard'),
                'type': 'ir.actions.act_window',
                'res_model': 'teacher.wizard',
                'view_id': self.env.ref('college_management.teacher_wizard_form_view').id,
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new',
                'context': {
                    'default_address': self.address,
                    'default_gender': self.gender
                }
            }
    
        return res


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



    teacher_id = fields.Many2one(
        comodel_name = "college.teacher",
        string="Teacher",
        domain=[('gender','=','female')],
        )

    @api.onchange('teacher_id')
    def onchange_teacher_id(self):
        if self.teacher_id:
            if self.teacher_id.gender:
                self.gender = self.teacher_id.gender
            else:
                self.gender = ''
        
            # if self.teacher_id.age:
            #     self.age = self.teacher_id.age
            # else:
            #     self.age = ''

    @api.onchange('gender')
    def onchange_gender(self):
        if self.gender == 'other':
            self.is_student = False
        else:
            self.is_student = True


    
    subject_ids = fields.Many2many(
        comodel_name="college.subject",
        relation = "student_subject_rel",
        column1 = "student_id",
        column2 = "subject_id",
        string="Subjects"
        )
    #name_get but not possible in odoo 17
    def name_get(self):
        teacher_list = []
        for record in self:
            print("\n\n\n\n\n:::",self)
            name = record.ref + record.name
            teacher_list.append((record.id,name))
        return teacher_list

    #mail sending

    def action_send_mail(self):
        template_id = self.env.ref('college_management.college_student_email_template_data').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
    

    # SMART BUTTON

    teacher_count = fields.Integer(string="Teacher Count", compute="_compute_teacher_count")

    def _compute_teacher_count(self):
        for rec in self:
            rec.teacher_count = self.env['college.teacher'].search_count([('student_id','=',rec.id)])
            print("\n\n\n\n.........",rec.teacher_count)
    

    def action_open_teachers(self):
        return {
            'type':'ir.actions.act_window',
            'name':'Students',
            'res_model':'college.teacher',
            'domain':[('student_id','=',self.id)],
            'view_mode':'tree,form',
            'target':'current',
        }
        

    fees_count = fields.Integer(string="Fees",compute="_compute_student_fees")

    def _compute_student_fees(self):
        for rec in self:
            rec.fees_count = self.env['college.fees'].search_count([('student_id','=',rec.id)])



    def action_student_fees_submitted(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Fees',
            'res_model':'college.fees',
            'domain': [('student_id','=',self.id)],
            'view_mode':'tree,form',
            'target':'current'
        }
   

    # special command

    