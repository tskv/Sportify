# -*- coding: utf-8 -*-


{
    'name': 'sportify',
    'version': '1.0',
    'category': 'Sport',
    'depends': ['base', 'mail'],
    'application': True,
    'installable': True,
    'images': ['static/description/icon.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/sportify_member_views.xml',
        'views/sportify_trainer_views.xml',
        'views/sportify_subscription_views.xml',
        'data/ir_cron.xml',
],
}