from odoo import models,fields,api


class Players(models.Model):
    _name="college.players"
    _description="players info"
 

    batsman_id = fields.Many2one(
        comodel_name = "college.batsman",
        string="Batsman"
        )
    
    name = fields.Char(string="Opposite Team")
    four = fields.Integer(string="Four")
    six = fields.Integer(string="Six")
    over = fields.Integer(string="Over")

    runs = fields.Integer(string=" Total Run",compute="_compute_runtotal")
    @api.depends('four','six')
    def _compute_runtotal(self):
        for rec in self:
            runs = (rec.four * 4) + (rec.six * 6)
            rec.runs = runs

   

