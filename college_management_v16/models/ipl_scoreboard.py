from odoo import models, fields,api
from odoo.exceptions import UserError

class Matches(models.Model):
    _name = 'college.matches'
    _description = 'IPL Scoreboard'
    _rec_name = "batsman_id"

    name = fields.Char(string="Match", default="IPL",readonly=True)
    is_calculation = fields.Boolean(string="Is Calculation?")

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
        # if not self.matches_line_ids:
        if not self.is_calculation:
            self.is_calculation = True
            batsman = self.env['college.players'].search([('batsman_id', '=', self.batsman_id.id)])
            for player in batsman:
                res = self.env['college.matches.line'].create(
                    {
                        "opp_team": player.name,
                        "four": player.four,
                        "six": player.six,
                        "over": player.over,
                        "run": player.runs,
                        "matches_id": self.id,
                    })

    def unlink(self):
        if self.matches_line_ids:
            raise UserError("you can not delete record.")
        return super(Matches,self).unlink()

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
    

