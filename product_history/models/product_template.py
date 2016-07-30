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


HISTORY_RANGE = [
    ('days', 'Days'),
    ('weeks', 'Week'),
    ('months', 'Month'),
]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_consumption_calculation_method(self):
        selection = super(ProductTemplate, self).\
            _get_consumption_calculation_method()
        selection.append(
            ('history', 'History (calculate consumption based on the Product\
            History)'),)
        return selection

# Columns section
    consumption_calculation_method = fields.Selection(
        _get_consumption_calculation_method,
        'Consumption Calculation Method', default='moves')
    history_range = fields.Selection(
        HISTORY_RANGE, "History Range", default="weeks")
    product_history_ids = fields.Many2many(
        comodel_name='product.history', inverse_name='product_tmpl_id',
        string='History', compute="_compute_product_history_ids")

# Private section
    @api.depends('history_range')
    @api.multi
    def _compute_product_history_ids(self):
        for template in self:
            template.product_history_ids.unlink()
            ph_ids = self.env['product.history'].search([
                ('product_tmpl_id', '=', template.id),
                ('history_range', '=', template.history_range)])
            ph_ids = [ph.id for ph in ph_ids]
            template.product_history_ids = [(6, 0, ph_ids)]
