# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SportifyMember(models.Model):
    _name = 'sportify.member'
    _description = 'Member'

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Name')
    mail = fields.Char(string='Mail')
    phone = fields.Integer(string='Phone')
    birth_date = fields.Date(string='Birth date')
    #membership_id = fields.Many2one(comodel_name='', string='Membership')
    inscription_date = fields.Date(string='Inscription date')

