from odoo import models, fields, api

class SportifySubscribtion(models.Model):
    _name = 'sportify.subscription'
    _description = 'Abonnement Salle de Sport'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name',required=True)
    member_id = fields.Many2one(comodel_name='sportify.member',required=True)
    duration_months = fields.Integer(string='Durée (mois)')
    type = fields.Selection([
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('vip', 'VIP')
    ], required=True)
    price = fields.Float()
    access = fields.Selection([
        ('10j', '10 jours'),
        ('30j', '30 jours'),
        ('illimite', 'Illimité')
    ])
    start_date = fields.Date(string='Start date')
    state= fields.Selection([
        ('activ', 'Active'),
        ('expired', 'Expired')
    ], default='activ')
    description = fields.Text()

    @api.onchange('type')
    def _onchange_type(self):
        if self.type == 'basic':
            self.access = '10j'
        elif self.type == 'premium':
            self.access = '30j'
        elif self.type == 'vip':
            self.access = 'illimite'

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        if 'start_date' in fields_list and not defaults.get('start_date'):
            defaults['start_date'] = fields.Date.today()
        return defaults

    @api.model_create_multi
    def create(self, vals):
        record = super().create(vals)
        message = f"Nouvel abonnement créé : {record.member_id.name}, {record.type}, {record.price}€"
        record.message_post(body=message)
        return record