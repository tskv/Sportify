# -*- coding: utf-8 -*-
{
    'name': "sportify",

    'summary': "Group project",

    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sportify_member_views.xml',
    ],
}