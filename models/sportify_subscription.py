from odoo import models, fields, api, exceptions

class SportifySubscription(models.Model):
    _name = 'sportify.subscription'
    _description = 'Sportify Subscription'
    _inherit = ['mail.thread']
    # même remarques, il faut le mail.activity.mixin


    @api.model
    def get_default_name(self):
        """Calculate unique name"""
        last_subscription =  self.search([], order="name desc", limit=1)
        if not last_subscription:
            return 'S0001'
        return 'S'+str(f"{int(last_subscription.name[1:])+1:04}")
    # Sachez qu'il y a un moyen plus simple pour faire cela : ir.sequence
    # si cela vous intéresse, vous pouvez aller voir mais c'est prévu qu'on le fasse dans 2 semaines

   # number = fields.Integer(default=get_default_number)
    name = fields.Char(string='Name', default=get_default_name, required=True)
    member_id = fields.Many2one(comodel_name='sportify.member',required=True)
    duration_months = fields.Integer(string='Duration (months)')
    type = fields.Selection([
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('vip', 'VIP')
    ], required=True)
    price = fields.Float()
    # si il  ya un prix, il faut rajouter la gestion de la currency (dollars, euro,etc)
    access = fields.Selection([
        ('10j', '10 days'),
        ('30j', '30 days'),
        ('illimite', 'Unlimited')
    ])
    start_date = fields.Date(string='Start date')
    end_date = fields.Date(string='End date', compute = '_compute_end_date')
    state = fields.Selection([
        ('ongoing', 'Ongoing'),
        ('expired', 'Expired')
    ], default='ongoing', required=True)
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
        if 'duration_months' in fields_list and not defaults.get('duration_months'):
            defaults['duration_months'] = 3
        return defaults

    @api.depends('start_date','duration_months')
    def _compute_end_date(self):
        """Calculates end_date"""
        for record in self:
            if record.start_date and record.duration_months:
                record.end_date = fields.Date.add(record.start_date, months=record.duration_months)
            else:
                record.end_date = fields.Date.today()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            member = self.env['sportify.member'].search([('id', '=', vals.get('member_id'))])
            # lorsque l'on souhaite retrouver un record avec un id, on peut utiliser le browse() qui est plus performant
            # cela ne s'utilise qu'avec l'id et donnerait ceci :
            # member = self.env['sportify.member'].browse(vals.get('member_id'))
            if vals.get('state') == 'ongoing' and member.number_active_subscriptions >= 1:
                raise exceptions.ValidationError("This member already has an active subscription")
            else:
                # techniquement, pas besoin du else, le raise arrête le code de toute façon
                record = super().create(vals)
                # attention , on ne créera pas de record les uns après les autres, create est fait pour tout créer en même temps
                # on créerait les records et ensuite on les updaterait comme ceci :
                # for vals in vals_list :
                #     member = self.env['sportify.member'].browse(vals.get('member_id'))
                #     if vals.get('state') == 'ongoing' and member.number_active_subscriptions >= 1:
                #         raise exceptions.ValidationError("This member already has an active subscription")
                # res = super().create(vals_list) # les records sont créés à ce moment-là
                # for rec in res :
                #     message = f"New subscription information: {rec.member_id.name}, {rec.type}, {rec.state}, {rec.price}€"
                #     rec.message_post(body=message)
                # return res
                message = f"New subscription information: {record.member_id.name}, {record.type}, {record.state}, {record.price}€"
                record.message_post(body=message)
                return record
