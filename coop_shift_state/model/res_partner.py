# -*- encoding: utf-8 -*-
##############################################################################
#
#    Purchase - Computed Purchase Order Module for Odoo
#    Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
#    @author Cyril Gaspard
from dateutil.relativedelta import relativedelta
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

from openerp import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta


STATES = [('up_to_day', 'Up to day'), ('alert', 'In alert'), ('suspended', 'Suspended'), ('delay', 'Delay'), 
          ('unsubscribed', 'Unsubscribed'), ('unpayed', 'Unpayed'), ('blocked', 'Blocked')]

SHIFT_TYPE = [('standard', 'Standard'), ('ftop', 'FTOP')]

class ResPartner(models.Model):
    _inherit = 'res.partner'

    state = fields.Selection(STATES)
    state_temp = fields.Selection(STATES)
    point_standard = fields.Integer('Classic points')
    point_ftop = fields.Integer('FTOP points')
    shift_delay = fields.Integer('Delay')
    date_alert_end  = fields.Date('End date alert')
    date_delay_end = fields.Date('End date delay')
    is_unpayed = fields.Boolean('Unpayed')
    is_blocked = fields.Boolean('Blocked')
    shift_type = fields.Selection(SHIFT_TYPE, 'Shift type')

    @api.model
    def create(self, vals):
        if vals.get('is_blocked'):
            vals['state'] = 'blocked'
        elif vals.get('is_unpayed'):
            vals['state'] = 'unpayed'
        state = vals.get('state')
        if 'point_standard' in vals:
            point_standard = vals['point_standard']
            if point_standard >= 0 and state != 'up_to_day' and state not in ['unpayed', 'blocked']:
                vals.update({'date_alert_end': False, 'state': 'up_to_day'})
            elif point_standard < 0 and state == 'up_to_day':
                date_alert_end = datetime.date.today() + relativedelta(days=27)
                vals.update({'state': 'alert', 'date_alert_end': date_alert_end})
        return super(ResPartner, self).create(vals)
        

    @api.multi
    def write(self, vals):
        if vals.get('is_blocked'):
            vals['state'] = 'blocked'
        elif vals.get('is_unpayed'):
            vals['state'] = 'unpayed'
        vals_state = vals.get('state')
        for record in self:
            state = vals_state or record.state
            if 'point_standard' in vals:
                point_standard = vals['point_standard']
                if point_standard >= 0 and state != 'up_to_day':
                    vals['date_alert_end'] = False
                    if state in ['alert', 'suspended', 'unsubscribed']:
                        vals['state'] = 'up_to_day'
                elif point_standard < 0:
                    if state == 'up_to_day':
                        date_alert_end = datetime.date.today() + relativedelta(days=28)
                        vals.update({'state': 'alert', 'date_alert_end': date_alert_end})
                    elif state == 'unsubscribed':
                        # TODO
                        print 'todo'
        return super(ResPartner, self).write(vals)
