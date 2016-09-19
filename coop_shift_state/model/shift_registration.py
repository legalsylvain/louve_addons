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

from openerp import models, fields, api


class ShiftRegistration(models.Model):
    _inherit = 'event.registration'

    product_temp_id = fields.Many2one('product.product', 'Product')
    shift_point = fields.Integer('Number of shift points')
    is_substitution = fields.Boolean()

    @api.one
    def update_partner_shift(self):
        partner = self.partner_id
        product_id = self.shift_ticket_id.product_id.id
        point = self._context.get('point', 0)
        self.write({'product_temp_id': product_id, 'shift_point': point})
        if product_id == self.env.ref('coop_shift.product_product_shift_standard'):
            partner.point_standard = partner.point_standard + point
        elif product_id == self.env.ref('coop_shift.product_product_shift_ftop'):
            partner.point_ftop = partner.point_ftop + point

    @api.one
    def button_reg_excused(self):
        res = super(ShiftRegistration, self).button_reg_excused()
        point = -1
        if self.is_substitution:
            point = 0
        self.with_context(nb_point=point).update_partner_shift()
        return res

    @api.one
    def button_reg_absent(self):
        res = super(ShiftRegistration, self).button_reg_absent()
        point = -2
        if self.is_substitution:
            point = -1
        self.with_context(nb_point=point).update_partner_shift()
        return res

    @api.one
    def _reset_point(self):
        product_temp_id = self.product_temp_id.id
        point = self.shift_point
        if point and product_temp_id == self.env.ref('coop_shift.product_product_shift_standard'):
            partner.point_standard = partner.point_standard - point
            
        elif point and product_temp_id == self.env.ref('coop_shift.product_product_shift_ftop'):
            partner.point_ftop = partner.point_ftop - point
        self.write({'product_temp_id': False, 'shift_point': 0})

    @api.one
    def button_reg_cancel(self):
        res = super(ShiftRegistration, self).button_reg_cancel()
        self._reset_point()
        return res

    @api.one
    def do_draft(self):
        res = super(ShiftRegistration, self).do_draft()
        self._reset_point()
        return res

    @api.one
    def button_reg_close(self):
        res = super(ShiftRegistration, self).button_reg_close()
        point = 0
        if self.is_substitution:
            point = 1
        self.with_context(nb_point=point).update_partner_shift()
        return res
