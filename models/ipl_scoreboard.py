from odoo import models, fields,api

class Matches(models.Model):
    _name = 'college.matches'
    _description = 'IPL Scoreboard'

    name = fields.Char(string="Match", default="IPL",readonly=True)
    
   
    matches_line_ids = fields.One2many(
        comodel_name = "college.matches.line",
        inverse_name = "matches_id",
        string = "Matches"
        )

    batsman_id = fields.Many2one(
        comodel_name = "college.batsman",
        string = "Batsman"
        )
    
    

    def action_record(self):
        batsman = self.env['college.players'].search([('batsman_id','=',self.batsman_id.id)])
        print("\n\n\n\n",batsman)
            
    
    total = fields.Integer(string="Total runs",compute="_compute_total")
    @api.depends('matches_line_ids','matches_line_ids.run')
    def _compute_total(self):
        for run in self:
            total = 0
            for rn in run.matches_line_ids:
                total += rn.run
            run.total = total


class MatchesLine(models.Model):
    _name = "college.matches.line"
    _description="matches info"
    
    opp_team = fields.Char(string="Opposite Team")
    four = fields.Integer(string="Four")
    six = fields.Integer(string="Six")
    over = fields.Integer(string="Over")
    run = fields.Integer(string="Run")
    #run_count = fields.Integer(string="Run Count")
    
    

    @api.onchange('batsman_id')
    def onchange_run_id(self):
        if self.batsman_id:
            self.run = self.batsman_id.runs
            self.four = self.batsman_id.four
            self.six = self.batsman_id.six
            self.over = self.batsman_id.over
    
   
    matches_id = fields.Many2one(
        comodel_name = "college.matches",
        string="matches"
        )

    # player_over = fields.Integer(string="over", compute="_compute_player_over")
    
    # @api.depends('batsman_id', 'matches_id.matches_line_ids')
    # def _compute_player_over(self):
    #     for record in self:
    #         player_name = record.batsman_id.name
    #         selection_count = sum(1 for line in record.matches_id.matches_line_ids if line.batsman_id.name == player_name)
    #         record.player_over = selection_count
    

