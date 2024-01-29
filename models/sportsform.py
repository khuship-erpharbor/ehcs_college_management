from odoo import models,fields,api,_
from odoo.exceptions import UserError,ValidationError
from datetime import datetime

class Sportsform(models.Model):
    _name = "college.sportsform"
    _description = "student info"

    name = fields.Char(string="Name" ,default=lambda self:_('New'))
    height = fields.Float(string="Height")
    gender = fields.Selection([
        ('male','Male'),
        ('female','Female'),
        ('others','Others')
        ],string="Gender")
    nationality = fields.Selection([
        ('indian','Indian'),
        ('other','Other')
        ],string = "Nationality")
    passportno = fields.Integer(string="Passport Number")
    visacard = fields.Integer(string="Visa Card")
    city = fields.Char(string="City")
    handicap = fields.Boolean(string="Handicap")
    govtassistance = fields.Boolean(string="Govt Assistance")
    assistance = fields.Char(string="Assistance")
    birthdate = fields.Date(string="Birth Date")
    age = fields.Float(string="Age")
    
    @api.constrains('age')
    def _age(self):
        for rec in self:
            if rec.age <=15:
                raise UserError("you won't participate in any sports")


    mobileno = fields.Char(string="Mobile Number")

    @api.constrains('mobileno')
    def _len_mobile(self):
        for num in self:
            if len(num.mobileno) != 10:
                raise UserError("You must enter 10 digit number")

    runningcapacity = fields.Selection([
        ('5km/hour','5 KM/Hour'),
        ('10km/hour','10 KM/Hour'),
        ('15km/hour','15 km/Hour')
        ],string="Running Capacity")


    @api.model
    def create(self,vals):
        """Called when new record is created
            SQL: insert into
            @param vals_list: List of Dict
            @return: recordsets
        """
        if vals.get('name',_('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('college.sportsform') or _('New')
        print("\n\n\n\n\nself::::::::",self)
        print("\n\n\n\n\nvals_list::::::::",vals)
        res = super(Sportsform, self).create(vals)
        print("\n\n\nres::::",res)
        #res['name'] = 'Ram'
        return res

    def write(self, vals):
        """Called when existing record is updated
            SQL: update table_name set name='sdfsd', dob='' where id in (21, 39)
            @return: True
        """
        print("\n\nwrite is called.........    ", self, vals)
        # Do something before record is updated
        if vals.get('nationality') == 'indian':
            self.handicap = True

        if vals.get('gender') == 'others':
            self.height = ''
        res = super(Sportsform, self).write(vals)


        # Do something after record is updated
        print("\n\n\n\nres::::::", res)
        return res

    def unlink(self):
        """Called when existing record is deleted
        SQL: delete from table_name where id in (34)
        @return: True
        """
        print("\n\nwrite is called.........    ", self)
        if self.handicap == True:
            raise UserError('Handicap Sport cannot be deleted.')
        return super(Sportsform, self).unlink()

    def copy(self, default=None):
        """
        Called when record is duplicated.
        It will call the create() method.
        @return: New recordset
        """
        print("\n\nCopy is called.........")
        sport_form = super(Sportsform, self).copy(default={'birthdate': datetime.now(), 'city': 'Mumbai'})
        print("sport_form......", sport_form)
        return sport_form

