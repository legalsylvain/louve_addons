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

from openerp import models, fields, api


class ReplaceRegistration(models.TransientModel):
    _inherit = 'replace.registration.wizard'

    
    state = fields.Selection([('absent', 'Absent'), ('excused', 'Excused'), ('waiting', 'Waiting')], required=True)

    # override function in module coop_shift
    @api.one
    def replace_member(self):
        registration = self.registration_id
        partner = self.partner_id
        new_partner = self.new_partner_id
        product_id = self.shift_ticket_id.product_id.id
        state = self.state
        vals = {'partner_id': new_partner_id.id,
                'state': 'replacing',
                'replaced_reg_id': registration.id,
                'tmpl_reg_line_id': False,
                'product_temp_id': product_id,
                'shift_point': 1,
                'is_substitution': True}
        new_reg_id = registration.copy(vals)
        if product_id == self.env.ref('coop_shift.product_product_shift_standard'):
            partner.point_standard = partner.point_standard - 1
            new_partner.point_standard = new_partner.point_standard + 1
        elif product_id == self.env.ref('coop_shift.product_product_shift_ftop'):
            partner.point_ftop = partner.point_ftop - 1
            new_partner.point_ftop = new_partner.point_ftop + 1
        registration.write({'state': 'replaced', 'product_temp_id': product_id, 'shift_point': point})
        self.replacing_reg_id = new_reg_id.id
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
