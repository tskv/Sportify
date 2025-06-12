# -*- coding: utf-8 -*-


{
    'name': 'sportify',
    'version': '1.0',
    # la version devrait aussi montrer la version odoo sur laquelle le module tourne
    # ici vous êtes en v18 donc la version devrait ressembler à : 18.1 ou 18.0.0.1
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
        'views/sportify_course_views.xml',
        'data/ir_cron.xml',
        # les data se mettent souvent en premier
    ],
}
