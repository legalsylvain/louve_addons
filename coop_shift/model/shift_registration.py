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

from openerp import models, fields, api, _
from openerp.exceptions import UserError

STATES = [
    ('cancel', 'Cancelled'),
    ('draft', 'Unconfirmed'),
    ('open', 'Confirmed'),
    ('done', 'Attended'),
    ('absent', 'Absent'),
    ('waiting', 'Waiting'),
    ('excused', 'Excused'),
    ('replaced', 'Replaced'),
    ('replacing', 'Replacing'),
]


class ShiftRegistration(models.Model):
    _inherit = 'event.registration'
    _name = 'shift.registration'
    _description = 'Attendee'

    event_id = fields.Many2one(required=False)
    shift_id = fields.Many2one(
        'shift.shift', string='Shift', required=True, ondelete='cascade')
    email = fields.Char(readonly=True, related='partner_id.email')
    phone = fields.Char(readonly=True, related='partner_id.phone')
    name = fields.Char(readonly=True, related='partner_id.name', store=True)
    partner_id = fields.Many2one(
        required=True, default=lambda self: self.env.user.partner_id)
    user_id = fields.Many2one(related="shift_id.user_id")
    shift_ticket_id = fields.Many2one(
        'shift.ticket', 'Shift Ticket', required=True, ondelete="cascade")
    state = fields.Selection(STATES)
    tmpl_reg_line_id = fields.Many2one(
        'shift.template.registration.line', "Template Registration Line")
    date_begin = fields.Datetime(related="shift_id.date_begin")
    date_end = fields.Datetime(related="shift_id.date_end")
    replacing_reg_id = fields.Many2one(
        'shift.registration', "Replacing Registration", required=False)
    replaced_reg_id = fields.Many2one(
        'shift.registration', "Replaced Registration", required=False)
    template_created = fields.Boolean("Created by a Template", default=False)
    shit_begin_date = fields.Datetime(
        string="Shift Start Date", related='shift_id.date_begin',
        readonly=True)

    _sql_constraints = [(
        'shift_registration_uniq',
        'unique (shift_id, partner_id)',
        'This partner is already registered on this Shift !'),
    ]

    @api.one
    @api.constrains('shift_ticket_id', 'state')
    def _check_ticket_seats_limit(self):
        if self.template_created:
            return True
        if self.shift_ticket_id.seats_max and\
                self.shift_ticket_id.seats_available < 0:
            raise UserError(_('No more available seats for this ticket'))

    @api.one
    def button_reg_absent(self):
        """ Mark as Absent """
        if self.event_id.date_begin <= fields.Datetime.now():
            self.state = 'absent'
        else:
            raise UserError(_("You must wait for the starting day of the shift\
                to do this action."))

    @api.one
    def button_reg_excused(self):
        """ Mark as Excused """
        if self.event_id.date_begin <= fields.Datetime.now():
            self.state = 'excused'
        else:
            raise UserError(_("You must wait for the starting day of the shift\
                to do this action."))
