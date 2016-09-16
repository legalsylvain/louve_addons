# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Compute Section
    @api.multi
    @api.depends('fundraising_partner_type_ids')
    def _compute_is_underclass_population(self):
        xml_id = self.env.ref('louve_membership.underclass_population_type').id
        for partner in self:
            partner.is_underclass_population =\
                xml_id in partner.fundraising_partner_type_ids.ids

    # Column Section
    is_louve_member = fields.Boolean('Is Louve Member')

    is_underclass_population = fields.Boolean(
        'is Underclass Population', compute=_compute_is_underclass_population)

    # View section
    @api.multi
    def set_underclass_population(self):
        xml_id = self.env.ref('louve_membership.underclass_population_type').id
        for partner in self:
            partner.fundraising_partner_type_ids = [(4, xml_id)]

    @api.multi
    def remove_underclass_population(self):
        xml_id = self.env.ref('louve_membership.underclass_population_type').id
        for partner in self:
            partner.fundraising_partner_type_ids = [(3, xml_id)]
