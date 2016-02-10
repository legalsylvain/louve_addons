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
import datetime


class ProductProduct(models.Model):
    _inherit = "product.product"

# Column section
    product_history_ids = fields.One2many(
        comodel_name='product.history', inverse_name='product_id',
        string='History', readonly=True)

# Private section
    @api.multi
    def _compute_qtys(self, states=('done',)):
        domain = [('state', 'in', states)] + self._get_domain_dates()
        for product in self:
            domain_product = domain + [('product_id', '=', product.id)]
            res = {
                'purchase_qty': 0,
                'view_qty': 0,
                'sale_qty': 0,
                'inventory_qty': 0,
                'procurement_qty': 0,
                'production_qty': 0,
                'transit_qty': 0, }
            move_pool = self.env['stock.move']

            for field, usage in (
                    ('purchase_qty', 'supplier'),
                    ('view_qty', 'view'),
                    ('sale_qty', 'customer'),
                    ('inventory_qty', 'inventory'),
                    ('procurement_qty', 'procurement'),
                    ('production_qty', 'production'),
                    ('transit_qty', 'transit'),
                    ):
                moves = move_pool.read_group(domain_product + [
                    ('location_id.usage', '=', usage),
                    ('location_dest_id.usage', '=', 'internal'),
                ], ['product_qty'], [])
                for move in moves:
                    res[field] = move['product_qty'] or 0
                moves = move_pool.read_group(domain_product + [
                    ('location_dest_id.usage', '=', usage),
                    ('location_id.usage', '=', 'internal'),
                ], ['product_qty'], [])
                for move in moves:
                    res[field] -= move['product_qty'] or 0
            return res

# Action section
    @api.model
    def run_product_history(self):
        # This method is called by the cron task
        products = self.env['product.product'].search([
            '|', ('active', '=', True),
            ('active', '=', False)])
        products._compute_history()

    @api.one
    def action_compute_history(self):
        self._compute_history()

    @api.multi
    def _compute_history(self):
        for product in self:
            if product.product_history_ids:
                self.env.cr.execute(
                    """SELECT to_date, end_qty FROM product_history
                    WHERE product_id=%s ORDER BY "id" DESC LIMIT 1"""
                    % (product.id))
                last_record = self.env.cr.fetchone()
                last_date = last_record and last_record[0] or None
                last_qty = last_record and last_record[1] or None
            else:
                last_date = "01/01/1900"
                last_qty = 0

            res = product.with_context({
                'from_date': last_date,
                'to_date': "%s" % (datetime.datetime.now())})._compute_qtys()
            res2 = product._product_available()[product.id]
            vals = {
                'product_id': product.id,
                'product_tmpl_id': product.product_tmpl_id.id,
                'location_id': self.env['stock.location'].search([])[0].id,
                'from_date': last_date,
                'to_date': "%s" % (datetime.datetime.now()),
                'purchase_qty': res['purchase_qty'],
                'sale_qty': res['sale_qty'],
                'loss_qty': res['inventory_qty'],
                'start_qty': last_qty,
                'end_qty': res2['qty_available'],
                'virtual_qty': res2['virtual_available'],
                'incoming_qty': res2['incoming_qty'],
                'outgoing_qty': res2['outgoing_qty'],
                }
            self.env['product.history'].create(vals)
