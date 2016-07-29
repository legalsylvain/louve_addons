# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    @api.constrains(
        'invoice_id.is_capital_souscription', 'product_id',
        'invoice_id.partner_id.accepted_category_ids')
    def check_capital_soucription(self):
        for line in self:
            print line
            pass  # TODO
