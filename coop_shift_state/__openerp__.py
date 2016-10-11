# -*- encoding: utf-8 -*-
##############################################################################
#
#    Purchase - Computed Purchase Order Module for Odoo
#    Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
#    @author Cyril Gaspard
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Coop Shift state',
    'version': '1.0',
    'category': 'Tools',
    'description': """
This module add state to partners depending of its attendees
    """,
    'author': 'Cyril Gaspard,'
              'Julien Weste',
    'website': '',
    'license': 'AGPL-3',
    'depends': [
        'coop_shift',
    ],
    'data': [
        'security/shift_security.xml',
        'views/res_partner_view.xml',
    ],
    'demo': [
    ],
}
