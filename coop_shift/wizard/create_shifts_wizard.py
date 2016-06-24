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
from datetime import datetime, timedelta
from openerp.exceptions import UserError


class CreateShifts(models.TransientModel):
    _name = 'create.shifts.wizard'
    _description = 'Create Shifts Wizard'

    @api.model
    def _get_last_shift_date(self):
        if self.template_ids:
            return min([t.last_shift_date for t in self.template_ids])
        elif self.env.context.get('active_ids', False):
            return min([
                t.last_shift_date for t in self.env['shift.template'].browse(
                    self.env.context['active_ids'])])
        else:
            return False

    @api.model
    def _get_default_date(self):
        lsd = self.last_shift_date or self._get_last_shift_date()
        if lsd:
            lsd = datetime.strptime(lsd, "%Y-%m-%d")
            return datetime.strftime(
                lsd + timedelta(days=1), "%Y-%m-%d")
        elif self.template_ids:
            return min([t.start_date for t in self.template_ids])
        else:
            return datetime.now()

    @api.model
    def _get_selected_templates(self):
        template_ids = self.env.context.get('active_ids', False)
        if template_ids:
            return template_ids
        template_id = self.env.context.get('active_id', False)
        if template_id:
            return template_id
        return []

    template_ids = fields.Many2many(
        'shift.template', 'template_createshift_rel', 'template_id',
        'wizard_id', string="Templates", default=_get_selected_templates)
    last_shift_date = fields.Date(
        'Last created shift date', default=_get_last_shift_date)
    date_from = fields.Date(
        'Plan this Template from', default=_get_default_date)
    date_to = fields.Date('Plan this Template until')

    @api.multi
    def create_shifts(self):
        for wizard in self:
            if wizard.date_from <= wizard.last_shift_date:
                raise UserError(_(
                    "'From date' can't be before 'Last shift date'"))
            for template in wizard.template_ids:
                rec_dates = template.get_recurrent_dates(
                    after=self.date_from, before=self.date_to)
                for rec_date in rec_dates:
                    rec_date = datetime(
                        rec_date.year, rec_date.month, rec_date.day)
                    date_begin = datetime.strftime(
                        rec_date + timedelta(hours=(template.start_time - 2)),
                        "%Y-%m-%d %H:%M:%S")
                    if date_begin.split(" ")[0] <= template.last_shift_date:
                        continue
                    date_end = datetime.strftime(
                        rec_date + timedelta(hours=(template.end_time - 2)),
                        "%Y-%m-%d %H:%M:%S")
                    rec_date = datetime.strftime(rec_date, "%Y-%m-%d")
                    vals = {
                        'shift_template_id': template.id,
                        'name': template.name,
                        'user_id': template.user_id.id,
                        'company_id': template.company_id.id,
                        'seats_max': template.seats_max,
                        'seats_availability': template.seats_availability,
                        'seats_min': template.seats_min,
                        'date_begin': date_begin,
                        'date_end': date_end,
                        'state': 'draft',
                        'reply_to': template.reply_to,
                        'address_id': template.address_id.id,
                        'description': template.description,
                        'shift_type_id': template.shift_type_id.id,
                        'week_number': template.week_number,
                        'shift_ticket_ids': None,
                    }
                    shift_id = self.env['shift.shift'].create(vals)
                    for ticket in template.shift_ticket_ids:
                        vals = {
                            'name': ticket.name,
                            'shift_id': shift_id.id,
                            'product_id': ticket.product_id.id,
                            'price': ticket.price,
                            'deadline': ticket.deadline,
                            'seats_availability': ticket.seats_availability,
                            'seats_max': ticket.seats_max,
                        }
                        ticket_id = self.env['shift.ticket'].create(vals)

                        for attendee in ticket.registration_ids:
                            state, strl_id = attendee._get_state(rec_date)
                            if state:
                                vals = {
                                    'partner_id': attendee.partner_id.id,
                                    'user_id': template.user_id.id,
                                    'state': state,
                                    'email': attendee.email,
                                    'phone': attendee.phone,
                                    'name': attendee.name,
                                    'shift_id': shift_id.id,
                                    'shift_ticket_id': ticket_id.id,
                                    'tmpl_reg_line_id': strl_id,
                                    'template_created': True,
                                }
                                self.env['shift.registration'].create(vals)
