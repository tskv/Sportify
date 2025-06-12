# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SportifyMember(models.Model):
    _name = 'sportify.member'
    _rec_name = 'name'
    _description = 'Member'
    _inherit = ['mail.thread']
    # pour le chatter, on hérite toujours comme ceci : _inherit = ['mail.thread', 'mail.activity.mixin']
    # sans le 2e modèle, on aura pas toutes les fonctionnalités du chatter

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Name', required=True)
    mail = fields.Char(string='Mail')
    phone = fields.Char(string='Phone')
    birth_date = fields.Date(string='Birth date', required=True)
    subscription_ids = fields.One2many(comodel_name='sportify.subscription', inverse_name='member_id', string='Subscription')
    inscription_date = fields.Date(string='Inscription date')
    photo = fields.Binary(string='Photo')
    age = fields.Integer(string='Age', compute = '_compute_age')
    subscription_type = fields.Char(string='Subscription type', compute = '_compute_subscription_type', store='True')
    course_ids = fields.Many2many(string="Courses", comodel_name="sportify.course")
    course_count = fields.Integer(compute='_compute_course_count')
    number_active_subscriptions = fields.Integer(compute='_compute_number_active_subscriptions', store='True')

    @api.model
    def default_get(self,fields_list):
        """Set the inscription_date to today's date by default"""
        defaults = super().default_get(fields_list)
        if 'inscription_date' in fields_list and not defaults.get('inscription_date'):
            defaults['inscription_date'] = fields.Date.today()
        return defaults
    # c'est correct mais il y a plus facile pour mettre ce défaut.
    # On peut le mettre directement dans le champ :
    # exemple :     date = fields.Date(string='Reversal date', default=fields.Date.context_today)


    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                record.age = today.year - record.birth_date.year - ((today.month, today.day) < (record.birth_date.month, record.birth_date.day))
            else:
                record.age = 0

    @api.depends('subscription_ids', 'subscription_ids.type', 'subscription_ids.state')
    def _compute_subscription_type(self):
        """Returns the type of the member's active subscription. If the member has no active subscriptions, returns 'basic'. """
        for record in self:
            record.subscription_type = 'basic'
            for subscription in record.subscription_ids:
                if subscription.state == 'ongoing':
                    record.subscription_type = subscription.type
                    break
        # Il n'y a pas de raison de faire un break (on essaye de les éviter au maximum)
        # + on peut éviter la boucle ce qui est plus performant en utilisant un filtered ()
        # on le verra en détails par la suite mais ça ressemblerait à ça :

        # for record in self:
        #     ongoing_sub_subscription = record.subscription_ids.filtered(lambda s: s.state == 'ongoing')
        #     if ongoing_sub_subscription:
        #         record.subscription_type = ongoing_sub_subscription[0].type
        #     else:
        #         record.subscription_type = 'basic'

        # et en contractant :

        # for record in self:
        #     if ongoing_sub_subscription := record.subscription_ids.filtered(lambda s: s.state == 'ongoing'):
        #         record.subscription_type = ongoing_sub_subscription[0].type
        #     else:
        #         record.subscription_type = 'basic'

    @api.depends('subscription_ids', 'subscription_ids.state')
    def _compute_number_active_subscriptions(self):
        """Returns the number of active subscriptions. Is checked before creating new subscription"""
        for record in self:
            number_active_subscriptions = 0
            for subscription in record.subscription_ids:
                if subscription.state == 'ongoing':
                    number_active_subscriptions += 1
            record.number_active_subscriptions = number_active_subscriptions
        # ici, vous pourriez également utiliser un filtered afin de ne pas faire de boucles
        # => len(record.subscription_ids.filtered(lambda s:s.state == 'ongoing'))

    @api.model_create_multi
    def create(self, vals):
        """Welcome message in chatter"""
        record = super().create(vals)
        # on aura tendance à écrire 'vals_list' comme paramètre pour ne pas oublier que c'est une liste de records qu'on reçoit
        message = f"Welcome to Sportify, {record.name}!"
        record.message_post(body=message)
        return record

    @api.depends('course_ids')
    def _compute_course_count(self):
        """ Number of courses the member has signed up for. Is used in statbutton. """
        for member in self:
            member.course_count = len(member.course_ids)

    def action_open_courses(self):
        """Action for a statbutton: opens list of courses for the member"""
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Courses',
            'res_model': 'sportify.course',
            'domain': [('id', 'in', self.course_ids.ids)],
            'views': [(False, 'list')],
            'context': {}
        }
        return action

    @api.model
    # pourquoi le @api.model ?
    def _action_cron_subscription_expired_soon(self):
        """Scheduled action: sends a message if the subscription expires in 1 week"""
        for member in self.search([]):
            for subscription in member.subscription_ids:
                if  fields.Date.add(subscription.end_date,weeks=-1) == fields.Date.today():
                    message_text = "The subscription expires in 1 week"
                    member.message_post(body=message_text)

