from odoo import models, fields, api


class SportifyCourse(models.Model):
    _name = "sportify.course"
    _description = "Cours Collectifs"

    name = fields.Char(required=True)
    trainer_id = fields.Many2one(string="Coach", comodel_name="sportify.trainer")
    date = fields.Date("Date")
    duration = fields.Integer(string="Duration", compute="_compute_duration")
    start_time = fields.Float("Start time")
    end_time = fields.Float("End time")
    max_number_participants = fields.Integer(string="Max number participants")
    fitness_room = fields.Char(string="Fitness room")
    member_ids = fields.Many2many(
        string="Members inscrits", comodel_name="sportify.member"
    )
    number_members = fields.Integer(string="Total Member")
    notes = fields.Text("Notes")
    active = fields.Boolean("Activ", default=True)
    member_count = fields.Integer("Number of Member", compute="_compute_total_member")
    course_photo = fields.Image("Course Photo")

    @api.depends("member_ids")
    def _compute_total_member(self):
        for record in self:
            record.member_count = len(record.member_ids)

    @api.depends("start_time", "end_time")
    def _compute_duration(self):
        for record in self:
            if record.start_time and record.end_time:
                record.duration = max(0, record.end_time - record.start_time)
            else:
                record.duration = 0

    def cancel_course(self):
        self.active = False
        message_text = "The course {} planed on {:%d-%m-%Y} at {}h is canceled".format(self.name, self.date, self.start_time)
        self.trainer_id.message_post(body=message_text)

