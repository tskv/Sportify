from odoo import models, fields, api


class SportifyCourses(models.Model):
    _name = "sportify.courses"
    _description = "Cours Collectifs"

    name = fields.Char(required=True)
    trainer_id = fields.Many2one(
        string="Coach", required=True, comodel_name="sportify.trainer"
    )
    date = fields.Date("Date")
    duration = fields.Integer(string="Duration", compute="_compute_duration")
    start_time = fields.Float("Start time", required=True)
    end_time = fields.Float("End time", required=True)
    max_number_participants = fields.Integer(string="Max number participants")
    fitness_room = fields.Char(string="Fitness room")
    members_ids = fields.Many2many(string="Membres inscrits")
    number_members = fields.Integer(string="Nombre membres inscrits")
    notes = fields.Text("Notes")
    active = fields.Boolean("Actif", default=True)

    @api.depends("start_time", "end_time")
    def _compute_duration(self):
        for record in self:
            if record.start_time and record.end_time:
                record.duration = max(0, record.end_time - record.start_time)
            else:
                record.duration = 0
