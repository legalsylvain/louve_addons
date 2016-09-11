# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Louve Custom - Capital Fundraising',
    'version': '9.0.0.0.0',
    'category': 'Custom',
    'summary': 'Custom settings for capital fundraising deployment',
    'author': 'La Louve',
    'website': 'http://www.lalouve.net',
    'depends': [
        'capital_fundraising',
    ],
    'data': [
        'security/ir_module_category.xml',
        'security/res_groups.xml',
        'views/view_res_partner.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
    ],
    'installable': True,
}
