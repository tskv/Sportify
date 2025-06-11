from odoo import models, fields, api, exceptions

class SportifySubscription(models.Model):
    _name = 'sportify.subscription'
    _description = 'Sportify Subscription'
    _inherit = ['mail.thread']


    @api.model
    def get_default_name(self):
        """Calculate unique name"""
        last_subscription =  self.search([], order="name desc", limit=1)
        if not last_subscription:
            return 'S0001'
        return 'S'+str(f"{int(last_subscription.name[1:])+1:04}")

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
            if vals.get('state') == 'ongoing' and member.number_active_subscriptions >= 1:
                raise exceptions.ValidationError("This member already has an active subscription")
            else:
                record = super().create(vals)
                message = f"New subscription information: {record.member_id.name}, {record.type}, {record.state}, {record.price}€"
                record.message_post(body=message)
                return record
