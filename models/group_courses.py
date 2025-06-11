from odoo import models, fields, api


class GroupCourses(models.Model):
    _name = "group.courses"
    _description = "Cours Collectifs"

    name = fields.Char(required=True)
    coach_id = fields.Many2one(string="Coach", required=True)
    date = fields.Date("Date")
    duration = fields.Integer(string="Duration")
    start_time = fields.Float("Start time", required=True)
    end_time = fields.Float("End time", required=True)
    max_number_participants = fields.Integer(string="Max number participants")
    fitness_room_id = fields.Many2one(string="Fitness room")
    membres_inscrits_ids = fields.Many2many(string="Membres inscrits")
    nombre_membres_inscrits = fields.Integer(string="Nombre membres inscrits")
    notes = fields.Text("Notes")
    active = fields.Boolean("Actif", default=True)

    @api.depends("start_time", "end_time")
    def _compute_duration(self):
        for record in self:
            if record.start_time and record.end_time:
                record.duration = max(0, record.end_time - record.start_time)
            else:
                record.duration = 0
