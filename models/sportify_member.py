# -*- coding: utf-8 -*-
from datetime import date

from odoo import models, fields, api

class SportifyMember(models.Model):
    _name = 'sportify.member'
    _description = 'Member'

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Name', required=True)
    mail = fields.Char(string='Mail')
    phone = fields.Integer(string='Phone')
    birth_date = fields.Date(string='Birth date', required=True)
    subscription_id = fields.Many2one(comodel_name='sportify.subscription', string='Subscription')
    inscription_date = fields.Date(string='Inscription date')
    photo = fields.Binary()
    age = fields.Integer(string='age', compute = '_compute_age')


    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = today.year - record.birth_date.year - ((today.month,today.day) < (record.birth_date.month, record.birth_date.day))
            else:
                record.age = 0



