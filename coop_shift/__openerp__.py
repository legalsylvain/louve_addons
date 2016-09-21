# -*- encoding: utf-8 -*-
##############################################################################
#
#    Purchase - Computed Purchase Order Module for Odoo
#    Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
#    @author Julien WESTE
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
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
    'name': 'Coop Shift',
    'version': '9.0.5',
    'category': 'Tools',
    'description': """
This module copys the event.event object to create a shift.shift object. This
will be used to define the working periods of the members of the LaLouve
cooperative, and other ones of the same type.
It also creates a shift.template object to help generating recurent shifts.

We define a config_parameter_weekA parameter to store the date of a Monday of
weekA (with format YYYY-MM-DD)

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2016-Today, Akretion;
    * Author :
        * Julien WESTE;
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com/fr',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'event',
        'event_sale',
        'mail',
    ],
    'data': [
        'wizard/create_shifts_wizard_view.xml',
        'wizard/update_shifts_wizard_view.xml',
        'wizard/add_template_registration_view.xml',
        'wizard/replace_registration_view.xml',
        'data/coop_shift_data.xml',
        'data/email_template_data.xml',
        'security/shift_security.xml',
        'views/menu.xml',
        'wizard/report_timesheet_wizard_view.xml',
        'wizard/report_wallchart_wizard_view.xml',
        'views/product_view.xml',
        'views/shift_mail_view.xml',
        'views/shift_registration_view.xml',
        'views/shift_template_registration_view.xml',
        'views/shift_template_registration_line_view.xml',
        'views/shift_shift_view.xml',
        'views/shift_template_view.xml',
        'wizard/create_shifts_wizard_view2.xml',
        'views/shift_type_view.xml',
        'views/res_partner_view.xml',
        'security/ir_model_access_data.yml',
        'security/ir_rule_data.yml',
        'security/ir_rule_data.xml',
        'data/module_data.xml',
        'views/shift_report.xml',
        'views/report_timesheet.xml',
        'views/report_wallchart.xml',
    ],
    'demo': [
        'data/shift_demo.xml',
    ],
}