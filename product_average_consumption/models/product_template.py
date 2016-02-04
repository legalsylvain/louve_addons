# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - Average Consumption Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
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


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Columns Section
    average_consumption = fields.Float(
        compute='_compute_average_consumption',
        string='Average Consumption per day', multi='average_consumption')
    total_consumption = fields.Float(
        compute='_compute_average_consumption',
        string='Total Consumption', multi='average_consumption')
    nb_days = fields.Integer(
        compute='_compute_average_consumption',
        string='Number of days for the calculation',
        multi='average_consumption',
        help="""The calculation will be done for the last 365 days or"""
        """ since the first purchase or sale of the product if it's"""
        """ more recent""")

    # Fields Function Section
    @api.multi
    def _compute_average_consumption(self):
        for template in self:
            nb_days = max(
                product.nb_days for product in template.product_variant_ids)
            total_consumption = sum(
                product.total_consumption
                for product in template.product_variant_ids)
            template.nb_days = nb_days
            template.total_consumption = total_consumption
            template.average_consumption = (
                nb_days and
                (total_consumption / nb_days) or False)
