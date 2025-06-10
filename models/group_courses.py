from odoo import models, fields, api

class GroupCourses(models.Model):
    _name = "group.courses"
    _description = 'Cours Collectifs'

    name = fields.Char(required=True)