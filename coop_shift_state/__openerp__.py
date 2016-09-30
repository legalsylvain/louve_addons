# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Cyril Gaspard
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Coop Shift state',
    'version': '1.0',
    'category': 'Tools',
    'description': """
This module add state to partners depending of its attendees
    """,
    'author': 'Cyril Gaspard,'
              'Julien Weste',
    'website': 'http://www.lalouve.net',
    'license': 'AGPL-3',
    'depends': [
        'coop_shift',
    ],
    'data': [
        'security/shift_security.xml',
        'views/view_res_partner.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
    ],
}
