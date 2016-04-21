# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Badge Reader',
    'version': '9.0.0.0.0',
    'category': 'Custom',
    'summary': 'Provide light Ionic Apps to read user Badge',
    'author': 'La Louve',
    'website': 'http://www.lalouve.net',
    'depends': [
        'base',
    ],
    'data': [
        'security/res_groups.xml',
        'views/view_res_partner.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
        'demo/res_users.xml',
        'demo/res_partner.xml',
    ],
    'installable': True,
}
