from odoo import fields, models

class SportifyTrainer (models.Model):
    _name = "sportify.trainer"
    _description = "sport center management"

    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="E-mail", required=True)
    phone = fields.Char(string="Phone number", required=True)
    speciality = fields.Char(string="Training Speciality", required=True)
    trainer_photo = fields.Image("Trainer Photo")