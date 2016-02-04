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

import time
import datetime
from openerp import models, fields, api
from openerp.tools.float_utils import float_round


class ProductProduct(models.Model):
    _inherit = "product.product"

    # Columns Section
    average_consumption = fields.Float(
        compute='_average_consumption',
        string='Average Consumption per day', multi='average_consumption')
    total_consumption = fields.Float(
        compute='_average_consumption',
        string='Total Consumption', multi='average_consumption')
    nb_days = fields.Integer(
        compute='_average_consumption',
        string='Number of days for the calculation',
        multi='average_consumption',
        help="""The calculation will be done for the last 365 days or"""
        """ since the first purchase or sale of the product if it's"""
        """ more recent""")

    # Private Function Section
    @api.one
    def _min_date(self, product_id):
        query = """SELECT to_char(min(date), 'YYYY-MM-DD') \
                from stock_move where product_id = %s""" % (product_id)
        cr = self.env.cr
        cr.execute(query)
        results = cr.fetchall()
        return results and results[0] and results[0][0] \
            or time.strftime('%Y-%m-%d')

    # Fields Function Section
    @api.multi
    def _average_consumption(self):
        first_date = time.strftime('%Y-%m-%d')
        begin_date = (
            datetime.datetime.today() -
            datetime.timedelta(days=365)).strftime('%Y-%m-%d')

        context = self.env.context or {}
        domain_products = [('product_id', 'in', self.ids)]
        domain_move_out = []
        dql, dmil, domain_move_out_loc = self._get_domain_locations()
        domain_move_out += self._get_domain_dates() + \
            [('state', 'not in', ('cancel', 'draft'))] + \
            domain_products
        if context.get('owner_id'):
            owner_domain = ('restrict_partner_id', '=', context['owner_id'])
            domain_move_out.append(owner_domain)
        domain_move_out += domain_move_out_loc
        moves_out = self.pool.get('stock.move').read_group(
            self.env.cr, self.env.uid, domain_move_out,
            ['product_id', 'product_qty'], ['product_id'], context=context)
        moves_out = dict(map(
            lambda x: (x['product_id'][0], x['product_qty']), moves_out))

        for product in self:
            first_date = max(
                begin_date,
                self._min_date(product.id)
            )
            outgoing_qty = float_round(
                moves_out.get(product.id, 0.0),
                precision_rounding=product.uom_id.rounding)
            nb_days = (
                datetime.datetime.today() -
                datetime.datetime.strptime(first_date, '%Y-%m-%d')
            ).days
            product.average_consumption = (
                nb_days and
                (outgoing_qty / nb_days) or False)
            product.total_consumption = outgoing_qty or False
            product.nb_days = nb_days or False
