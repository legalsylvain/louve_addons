# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Capital Souscription',
    'version': '9.0.0.0.0',
    'category': 'Accounting',
    'summary': 'Provide extra accounting features for capital souscription',
    'author': 'La Louve',
    'website': 'http://www.lalouve.net',
    'depends': [
        'account',
    ],
    'data': [
        'views/view_capital_fundraising_wizard.xml',
        'views/view_product_template.xml',
        'views/view_res_partner.xml',
        'views/view_account_payment.xml',
        'views/view_account_invoice.xml',
        'views/view_capital_fundraising_category.xml',
        'views/view_capital_fundraising.xml',
        'views/action.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
    ],
    'installable': True,
}
