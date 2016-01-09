# -*- encoding: utf-8 -*-
##############################################################################
#
#    Purchase - Package Quantity Module for Odoo
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

from math import ceil

from openerp.osv.osv import except_osv
from openerp import api, models, _


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # Constraints section
    # TODO: Rewrite me in _contraint, if the Orm V8 allows param in message.
    @api.one
    @api.constrains('order_id', 'product_id', 'product_qty')
    def _check_purchase_qty(self):
        for pol in self:
            if pol.order_id.state not in ('draft', 'sent'):
                continue
            if not pol.product_id:
                return True
            supplier_id = pol.order_id.partner_id.id
            found = False
            for psi in pol.product_id.seller_ids:
                if psi.name.id == supplier_id:
                    package_qty = psi.package_qty
                    indicative = psi.indicative_package
                    found = True
                    break
            if not found:
                return True
            if not indicative:
                if (int(pol.product_qty / package_qty) !=
                        pol.product_qty / package_qty):
                    raise except_osv(
                        _("Package Error!"),
                        _(
                            """You have to buy a multiple of the package"""
                            """ qty or change the package settings in the"""
                            """ supplierinfo of the product for the"""
                            """ following line:"""
                            """ \n - Product: %s;"""
                            """ \n - Quantity: %s;"""
                            """ \n - Unit Price: %s;""" % (
                                pol.product_id.name, pol.product_qty,
                                pol.price_unit)))

    @api.model
    def create(self, vals):
        res = super(PurchaseOrderLine, self).create(vals)
        self._check_purchase_qty([res])
        return res

    @api.multi
    def write(self, vals):
        res = super(PurchaseOrderLine, self).write(vals)
        self._check_purchase_qty()
        return res

    # Views section
    @api.onchange('product_qty', 'product_uom')
    def onchange_product_qty(self):
        res = {}
        if self.product_id:
            product = self.product_id
            for supplier in product.seller_ids:
                if self.partner_id and (supplier.name == self.partner_id):
                    self.package_qty = supplier.package_qty
                    self.indicative = supplier.indicative_package
                    if (not(self.indicative) and
                            int(self.product_qty / self.package_qty) !=
                            self.product_qty / self.package_qty):
                        res['warning'] = {
                            'title': _('Warning!'),
                            'message': _(
                                """The selected supplier only sells"""
                                """this product by %s %s""") % (
                                supplier.package_qty,
                                supplier.product_uom.name)}
                        self.product_qty = ceil(self.product_qty /
                            self.package_qty) * self.package_qty
        return res
