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
    color = fields.Integer(compute = '_compute_color', store='True')
    member_type = fields.Char(string='Member type', compute = '_compute_member_type', store='True')

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
    def _compute_member_type(self):
        for record in self:
            best_type = 'Basic'
            if record.subscription_ids:
                for subscription in record.subscription_ids:
                    if subscription.state == 'active' and subscription.type == 'vip':
                        best_type = 'VIP'
                        break
                    if subscription.state == 'active' and subscription.type == 'premium' and best_type != 'VIP':
                        best_type = 'Premium'
            record.member_type = best_type


    @api.depends('subscription_ids')
    def _compute_color(self):
        for record in self:
            if record.member_type == 'VIP':
                record.color = 7
            else:
                record.color = 0


    @api.model_create_multi
    def create(self, vals):
        record = super().create(vals)
        message = f"Welcome to Sportify, {record.name}!"
        record.message_post(body=message)
        return record

    @api.model
    def _action_cron_subscription_expired_soon(self):
        for member in self.search([]):
            for subscription in member.subscription_ids:
                if  fields.Date.add(subscription.end_date,weeks=-1) == fields.Date.today():
                    message_text = "The subscription expires in 1 week"
                    member.message_post(body=message_text)



