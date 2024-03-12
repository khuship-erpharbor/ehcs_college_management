from odoo import models,fields,api


class Batsman(models.Model):
    _name="college.batsman"
    _description="batsman info"
 

    name = fields.Char(string="Batsman Name")
    # four = fields.Integer(string="Four")
    # six = fields.Integer(string="Six")
    # runs = fields.Integer(string=" Total Run")

   

