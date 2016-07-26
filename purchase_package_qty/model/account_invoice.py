# -*- encoding: utf-8 -*-
##############################################################################
#
#    Purchase - Package Quantity Module for Odoo
#    Copyright (C) 2016-Today Akretion (https://www.akretion.com)
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

from openerp import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('purchase_id')
    def purchase_order_change(self):
        res = super(AccountInvoice, self).purchase_order_change()
        for line in self.invoice_line_ids:
            line.price_policy = line.purchase_line_id.price_policy
            line.quantity = line.purchase_line_id.product_qty
            line.package_qty = line.purchase_line_id.package_qty
            line.product_qty_package =\
                line.purchase_line_id.product_qty_package
        return res
