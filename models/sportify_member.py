# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SportifyMember(models.Model):
    _name = 'sportify.member'
    _rec_name = 'name'
    _description = 'Member'
    _inherit = ['mail.thread']

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Name', required=True)
    mail = fields.Char(string='Mail')
    phone = fields.Char(string='Phone')
    birth_date = fields.Date(string='Birth date', required=True)
    subscription_ids = fields.One2many(comodel_name='sportify.subscription', inverse_name='member_id', string='Subscription')
    inscription_date = fields.Date(string='Inscription date')
    photo = fields.Binary(string='Photo')
    age = fields.Integer(string='Age', compute = '_compute_age')
    color = fields.Integer(compute = '_compute_color')

    @api.model
    def default_get(self,fields_list):
        defaults = super().default_get(fields_list)
        if 'inscription_date' in fields_list and not defaults.get('inscription_date'):
            defaults['inscription_date'] = fields.Date.today()
        return defaults

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                record.age = today.year - record.birth_date.year - ((today.month, today.day) < (record.birth_date.month, record.birth_date.day))
            else:
                record.age = 0

    @api.depends('subscription_ids')
    def _compute_color(self):
        for record in self:
            record.color = 0
            if record.subscription_ids:
                for subscription in record.subscription_ids:
                    if subscription.type == 'vip':
                        record.color = 7
                        break


    @api.model_create_multi
    def create(self, vals):
        record = super().create(vals)
        message = f"Welcome to Sportify, {record.name}!"
        record.message_post(body=message)
        return record

    @api.model
    def action_cron_subscription_expired_soon(self):
        for member in self.search([]):
            if member.subscription_id:
                expire_date = fields.Date.add(member.inscription_date, months=member.subscription_id.duration_months)
                if fields.Date.today() ==  fields.Date.add(expire_date,weeks=-1):
                    message_text = "The subscription expires in 1 week"
                    member.message_post(body=message_text)



