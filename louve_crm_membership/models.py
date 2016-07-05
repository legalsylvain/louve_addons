# -*- coding: utf-8 -*-
##############################################################################
#
#    Author:Aurélien Dumaine, LaLouve@Paris
#    Copyright (C) 2014 Agile Business Group (<http://www.agilebg.com>)
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

from openerp import models, fields


class louve_crm_contact_origin(models.Model):
    _name = 'res.contact_origin'
    name = fields.Char()
    partner_ids = fields.One2many(
        comodel_name="res.partner", inverse_name="contact_origin_id",
        string="Members")


class louve_crm_membership(models.Model):
    # @api.multi
    # def onchange_type(self, is_company):
    #     # FIXME : why do we do this ? it's already done in the standard
    #     # module??
    #     res = super(louve_crm_membership, self).onchange_type(is_company)
    #     if 'invisible' not in res :
    #         res.update({'invisible':{}})
    #     if self.is_company:
    #         res['invisible']['company_id'] = False
    #     else:
    #         res['invisible']['company_id'] = True
    #     return res

    _inherit = 'res.partner'

    contact_origin_id = fields.Many2one(
        comodel_name="res.contact_origin", string="Contact Origin")
    company_type_id = fields.Many2one(
        comodel_name="res.company_type", string="Company Type")
    is_deceased = fields.Boolean("Is Deceased")
    adult_number_in_family = fields.Integer(
        string="Nb adults", help="Number of adults in the family")


class louve_crm_company_type(models.Model):
    _name = 'res.company_type'
    name = fields.Char()
    partner_ids = fields.One2many(
        comodel_name="res.partner", inverse_name="company_type_id",
        string="Company Type")
