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
from datetime import datetime, timedelta


class ShiftShift(models.Model):
    _inherit = 'event.event'
    _name = 'shift.shift'
    _description = 'Shift Template'

    @api.model
    def _default_shift_mail_ids(self):
        return [(0, 0, {
            'interval_unit': 'now',
            'interval_type': 'after_sub',
            'template_id': self.env.ref('coop_shift.shift_subscription')
        })]

    name = fields.Char(string="Shift Name")
    event_mail_ids = fields.One2many(default=None)
    shift_mail_ids = fields.One2many(
        'shift.mail', 'shift_id', string='Mail Schedule',
        default=lambda self: self._default_shift_mail_ids())
    shift_type_id = fields.Many2one(
        'shift.type', string='Category', required=False,
        readonly=False, states={'done': [('readonly', True)]})
    week_number = fields.Selection(
        [(1, 'Week A'), (2, 'Week B'), (3, 'Week C'), (4, 'Week D')],
        string='Week', required=True)
    registration_ids = fields.One2many(
        'shift.registration', 'shift_id', string='Attendees',
        readonly=False, states={'done': [('readonly', True)]})
    shift_template_id = fields.Many2one('shift.template', string='Template')
    seats_reserved = fields.Integer(compute='_compute_seats_shift')
    seats_available = fields.Integer(compute='_compute_seats_shift')
    seats_unconfirmed = fields.Integer(compute='_compute_seats_shift')
    seats_used = fields.Integer(compute='_compute_seats_shift')
    seats_expected = fields.Integer(compute='_compute_seats_shift')
    auto_confirm = fields.Boolean(
        string='Confirmation not required', compute='_compute_auto_confirm')
    event_ticket_ids = fields.One2many(
        default=lambda rec: rec._default_tickets())
    shift_ticket_ids = fields.One2many(
        'shift.ticket', 'shift_id', string='Shift Ticket',
        default=lambda rec: rec._default_shift_tickets(), copy=True)
    date_tz = fields.Selection('_tz_get', string='Timezone', default=False)
    date_without_time = fields.Datetime(
        string='Date', compute='_get_date_without_time', store=True)
    begin_time = fields.Float(
        string='Start Time', compute='_get_begin_time', store=True)
    end_time = fields.Float(
        string='Start Time', compute='_get_end_time', store=True)

    _sql_constraints = [(
        'template_date_uniq',
        'unique (shift_template_id, date_begin, company_id)',
        'The same template cannot be planned several time at the same date !'),
    ]

    @api.model
    def _default_tickets(self):
        return

    @api.model
    def _default_shift_tickets(self):
        try:
            product = self.env.ref('coop_shift.product_product_shift_standard')
            product2 = self.env.ref('coop_shift.product_product_shift_ftop')
            return [
                {
                    'name': _('Standard'),
                    'product_id': product.id,
                    'price': 0,
                },
                {
                    'name': _('FTOP'),
                    'product_id': product2.id,
                    'price': 0,
                }]
        except ValueError:
            return self.env['shift.ticket']

    @api.one
    @api.constrains('seats_max', 'seats_available')
    def _check_seats_limit(self):
        if self.seats_availability == 'limited' and self.seats_max and\
                self.seats_available < 0:
            raise UserError(_('No more available seats.'))

    @api.one
    def _compute_auto_confirm(self):
        self.auto_confirm = False

    @api.model
    def _default_event_mail_ids(self):
        return None

    @api.multi
    @api.depends('seats_max', 'registration_ids.state')
    def _compute_seats_shift(self):
        """ Determine reserved, available, reserved but unconfirmed and used
        seats. """
        # initialize fields to 0
        for shift in self:
            shift.seats_unconfirmed = shift.seats_reserved =\
                shift.seats_used = shift.seats_available = 0
        # aggregate registrations by shift and by state
        if self.ids:
            state_field = {
                'draft': 'seats_unconfirmed',
                'open': 'seats_reserved',
                'replacing': 'seats_reserved',
                'done': 'seats_used',
            }
            query = """ SELECT shift_id, state, count(shift_id)
                        FROM shift_registration
                        WHERE shift_id IN %s
                        AND state IN ('draft', 'open', 'done', 'replacing')
                        GROUP BY shift_id, state
                    """
            self._cr.execute(query, (tuple(self.ids),))
            for shift_id, state, num in self._cr.fetchall():
                shift = self.browse(shift_id)
                shift[state_field[state]] += num
        # compute seats_available
        for shift in self:
            if shift.seats_max > 0:
                shift.seats_available = shift.seats_max - (
                    shift.seats_reserved + shift.seats_used)
            shift.seats_expected = shift.seats_unconfirmed +\
                shift.seats_reserved + shift.seats_used

    @api.multi
    def write(self, vals):
        for shift in self:
            if shift.state == "done":
                raise UserError(_(
                    'You can only repercute changes on draft shifts.'))
        return super(ShiftShift, self).write(vals)

    @api.onchange('shift_template_id')
    def _onchange_template_id(self):
        if self.shift_template_id:
            self.name = self.shift_template_id.name
            self.user_id = self.shift_template_id.user_id
            self.shift_type_id = self.shift_template_id.shift_type_id
            self.week_number = self.shift_template_id.week_number
            cur_date = self.date_begin and datetime.strptime(
                self.date_begin, "%Y-%m-%d %H:%M:%S").date() or\
                datetime.strptime(
                    self.shift_template_id.start_date, "%Y-%m-%d")
            self.date_begin = datetime.strftime(
                cur_date + timedelta(
                    hours=self.shift_template_id.start_time),
                "%Y-%m-%d %H:%M:%S")
            self.date_end = datetime.strftime(
                cur_date + timedelta(
                    hours=self.shift_template_id.end_time),
                "%Y-%m-%d %H:%M:%S")

            cur_attendees = [r.partner_id.id for r in self.registration_ids]
            vals = []
            for attendee in self.shift_template_id.registration_ids:
                if attendee.id not in cur_attendees:
                    vals.append((0, 0, {
                        'partner_id': attendee.id,
                        'state': 'draft',
                        'email': attendee.email,
                        'phone': attendee.phone,
                        'name': attendee.name,
                        'shift_id': self.id,
                    }))
                self.registration_ids = vals

    @api.multi
    @api.depends('date_begin')
    def _get_date_without_time(self):
        for shift in self:
            shift.date_without_time = datetime.strftime(datetime.strptime(
                shift.date_begin, "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d")

    @api.model
    def _convert_time_float(self, t):
        return (((
            float(t.microsecond) / 1000000) + float(t.second) / 60) + float(
            t.minute)) / 60 + t.hour

    @api.multi
    @api.depends('date_begin')
    def _get_begin_time(self):
        for shift in self:
            shift.begin_time = self._convert_time_float(datetime.strptime(
                shift.date_begin, "%Y-%m-%d %H:%M:%S").time())

    @api.multi
    @api.depends('date_end')
    def _get_end_time(self):
        for shift in self:
            shift.end_time = self._convert_time_float(datetime.strptime(
                shift.date_end, "%Y-%m-%d %H:%M:%S").time())
