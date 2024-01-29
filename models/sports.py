from odoo import models,fields

class Sports(models.Model):
    _name = "college.sports"
    _description = "Sports Information"


    name = fields.Char(string="Game Name")
    fees = fields.Float(string="Fees")


    
    # Many2one field referencing bowler's name in college.matches
    # bowler_id = fields.Many2one(
    #     comodel_name="college.matches",
    #     string="Bowler",
    #     )
    
     # total_appearances = fields.Integer(
    #     string="Total Appearances",
    #     compute="_compute_total_appearances",
    #     store=True  # To store the computed value in the database
    # )

    # @api.depends('matches_id')
    # def _compute_total_appearances(self):
    #     for record in self:
    #         record.total_appearances = self.env['college.matches.line'].search_count(
    #             [('cricketer', '=', record.cricketer)])


   