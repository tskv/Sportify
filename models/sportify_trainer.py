from odoo import fields, models, api

class SportifyTrainer (models.Model):
    _name = "sportify.trainer"
    _description = "sport center management"

    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="E-mail", required=True)
    phone = fields.Char(string="Phone number", required=True)
    speciality = fields.Selection([('judo', 'Judo'), ('yoga', 'Yoga'), ('gym', 'Gym'), ('tennis', 'Tennis')])
    trainer_photo = fields.Image("Trainer Photo")
    courses_ids = fields.One2many(
        comodel_name='sportify.courses',
        inverse_name='trainer_id',
        string='Courses'
    )
    courses_count = fields.Integer('Number of Courses', compute='_compute_total_courses')

    @api.depends("courses_ids")
    def _compute_total_courses(self):
        for record in self:
            record.courses_count = len(record.courses_ids)

    def action_get_courses(self):
        return {
            'name':'Trainer courses',
            'view_mode': 'list,form',
            'res_model':'sportify.courses',
            'type': 'ir.actions.act_window',
        }