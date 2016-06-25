# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Smile (<http://www.smile.fr>). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'La Louve Membership Profile',
    'version': '1.0',
    'depends': [
        'purchase',
        'sale',
        'project',
        'web_printscreen_zb',
        'account',
        'account_voucher',
        'l10n_fr',
        'membership',
        'calendar',
        'smile_access_control',
        'louve_crm_membership',
        'louve_accounting_profile',
        # 'smile_base',
    ],
    'author': 'La Louve',
    'description': """
    Module profil pour le lot gestion des membres \n
    """,
    'summary': 'Company data & Dependencies',
    'website': 'http://www.cooplalouve.fr',
    'category': 'Profile',
    'sequence': 10,
    'data': [],
    # 'views/res_partner_view.xml',
    # 'data/company_data.xml',

    'auto_install': False,
    'installable': True,
    'application': False,
}
