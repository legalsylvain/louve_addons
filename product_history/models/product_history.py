# *- encoding: utf-8 -*-
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

from openerp import models, fields

HISTORY_RANGE = [
        ('days', 'Days'),
        ('weeks', 'Week'),
        ('months', 'Month'),
        ]


class ProductHistory(models.Model):
    _name = "product.history"

# Columns section
    product_id = fields.Many2one(
        comodel_name='product.product', string='Product',
        required=True, ondelete='cascade')
    product_tmpl_id = fields.Many2one(
        'product.template', related='product_id.product_tmpl_id',
        string='Template', store=True)
    location_id = fields.Many2one(
        'stock.location', string='Location', required=True,
        ondelete='cascade')
    from_date = fields.Date("From Date")
    to_date = fields.Date("To Date")
    purchase_qty = fields.Float("Purchases")
    production_qty = fields.Float("Production")
    sale_qty = fields.Float("Sales")
    loss_qty = fields.Float("Losses")
    start_qty = fields.Float("Opening quantity")
    end_qty = fields.Float("Closing quantity")
    incoming_qty = fields.Float("Incoming quantity")
    outgoing_qty = fields.Float("Outgoing quantity")
    virtual_qty = fields.Float("Virtual quantity")
